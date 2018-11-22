import ProxyRule
import re

def swap(text, x, y):
    x, y = bytes(x, 'utf-8'), bytes(y, 'utf-8')
    return re.sub(x + b'|' + y, lambda m: x if m.group() == y else y, text)

class Swap:
    def response(self, flow):
        flow.response.content = swap(flow.response.content, "Fire", "Water")

    def ProxyRule(self, port):
        return ProxyRule.ProxyRule(host="*.wikipedia.org", port=port)

    def __str__(self):
        return self.__class__.__name__