import requests
import ai.model as ai
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse


class CrawlerSearchNode(ai.SearchNode):

    def __init__(self, target, state, d=0, p=0, a=None, visited_states=[]):
        super().__init__(state, d, p, a)
        self.target = target
        self.visited_states = visited_states

    @classmethod
    def from_copy(cls, node, visited_states):
        return cls(node.target, node.state, node.d, node.p, node.a, visited_states)

    def expand(self):
        print('Expand: ' + self.state)
        expanded = []

        try:
            response = requests.get(self.state)
        except requests.exceptions.RequestException:
            print('Error - Could not expand: ' + self.state)
            return []

        if response.status_code != 200:
            return []

        for link in BeautifulSoup(markup=response.text, features='html.parser', parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                url = CrawlerSearchNode.parse(link['href'])
                if not CrawlerSearchNode.valid_url(url):
                    continue

                url_key = CrawlerSearchNode.hostname(url)
                if url_key not in self.visited_states or CrawlerSearchNode.test_goal(self.target, url):
                    self.visited_states.append(url_key)
                    expanded.append(CrawlerSearchNode(self.target, url, self.d + 1, self.p + 1, self.state))

        return list(map(lambda node: CrawlerSearchNode.from_copy(node, self.visited_states), expanded))

    def is_goal(self):
        return CrawlerSearchNode.test_goal(self.target, self.state)

    @staticmethod
    def test_goal(target, state):
        return state.find(target) > -1

    @staticmethod
    def valid_url(url):
        return url.find('http') > -1 or url.find('https') > -1

    @staticmethod
    def parse(url):
        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    @staticmethod
    def hostname(url):
        parsed_uri = urlparse(url)
        return '{uri.netloc}'.format(uri=parsed_uri)


def find_path(from_url, to_url):
    start_node = CrawlerSearchNode(to_url, from_url)
    return ai.search(start_node, ai.BestFirstStrategy())
