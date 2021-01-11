import unittest
from exercises.excel import send


class SendMailTest(unittest.TestCase):

    def test_send(self):
        username = "ritzl1"
        file: str = 'resources/marking-exercise.xlsx'

        # Act
        send(username, file)
