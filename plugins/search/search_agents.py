import webbrowser
import garcon.plugin


def build_bing_url(query):
    query_part = '+'.join(query.strip().split(' '))
    return "http://bing.com/search?q=%s" % (query_part)


class SearchAgent(garcon.plugin.AgentBase):
    name = "SearchAgent"
    priority = 4

    def can_handle(self, command):
        return command.startswith("bing")

    def handle(self, command):
        query = command.replace("bing", "")
        url = build_bing_url(query)
        webbrowser.open(url)
        