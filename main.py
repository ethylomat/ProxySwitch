import multiprocessing
import os, platform
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from http.server import BaseHTTPRequestHandler, HTTPServer

from addons import swap

addons = [
    swap.Swap(),
]

class ProxyMaster(DumpMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, **kwargs):
        try:
            DumpMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

def startProxyProcess(port, addon):
    print("Starting proxy process on port %s with addon: %s" % (str(port), str(addon)))
    options = Options(listen_host='0.0.0.0', listen_port=port, http2=True)
    options.add_option("body_size_limit", int, 0, "")
    options.add_option("keep_host_header", bool, True, "")
    config = ProxyConfig(options)
    master = ProxyMaster(options, with_termlog=False, with_dumper=False)
    master.server = ProxyServer(config)
    master.addons.add(addon)
    master.run()

class ConfigurationHTTPRequestHandler(BaseHTTPRequestHandler):
    rules = []

    def __init__(self, *args):
        super(ConfigurationHTTPRequestHandler, self).__init__(*args)

    def addRule(self, ProxyRule):
        self.rules.append(ProxyRule)

    def setRules(self, rules):
        self.rules = rules

    def getRules(self):
        return [r.toText() for r in self.rules]

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/x-ns-proxy-autoconfig') # 'application/octet-stream'
        self.end_headers()
        rule_pac = "function FindProxyForURL(url, host) { \n" + ("\n".join(self.getRules()) + 'return "DIRECT";\n}').rstrip()
        self.wfile.write(bytes(str(rule_pac), 'utf8'))


def startProxyConfigurationServer(server_class=HTTPServer, handler_class=ConfigurationHTTPRequestHandler, port=8000, rules=[]):
    server_address = ('', port)
    handler_class.setRules(handler_class, rules)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd process on port {}'.format(port))
    httpd.serve_forever()


if __name__ == '__main__':
    processes = []
    rules = []

    port = 8080

    for addon in addons:
        port = port + 1
        p = multiprocessing.Process(target=startProxyProcess, args=(port, addon,))
        p.start()

        rule = addon.ProxyRule(port)
        rules.append(rule)
        processes.append(p)

    configServer = multiprocessing.Process(target=startProxyConfigurationServer, args=(HTTPServer, ConfigurationHTTPRequestHandler, 8000, rules))
    configServer.start()

    if platform.system() == "Darwin":
        os.system("./helper_scripts/reload_pac.sh")

    configServer.join()

    for p in processes:
        p.join()