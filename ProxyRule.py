class ProxyRule:
    def __init__(self, url_scheme=None, url_schemes=[], host=None, hosts=[], port=None):
        if type(port) != int:
            raise TypeError('Type is not int')
        self.url_schemes = url_schemes
        if url_scheme is not None:
            self.url_schemes = []
            self.url_schemes.append(url_scheme)
        self.hosts = hosts
        if host is not None:
            self.hosts = []
            self.hosts.append(host)
        self.port = str(port)

    def url_rule(self, url_scheme):
        return 'shExpMatch(url, "%s")' % (url_scheme)

    def host_rule(self, host):
        return 'shExpMatch(host,"%s")' % (host)

    def generate_conditions(self):
        url_rules = [self.url_rule(url_scheme) for url_scheme in self.url_schemes]
        host_rules = [self.host_rule(host) for host in self.hosts]
        return " || ".join(host_rules + url_rules)

    def toText(self):
        text = """
        if (%s){
            return "PROXY 127.0.0.1:%s";
        }
        """ % (self.generate_conditions(), self.port)
        return text

    def __str__(self):
        return self.toText()
