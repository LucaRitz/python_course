import unittest
import ai.crawler as crawler


class CrawlerTest(unittest.TestCase):

    def test_bfhFound(self):
        # Act
        result = crawler.find_path('http://www.gnu.org', 'bfh.ch')

        # Assert
        self.assertIsNotNone(result)
        print(result.p)
