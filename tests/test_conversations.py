from unittest import TestCase
from chatterbot.conversation import Statement


class StatementTests(TestCase):

    def setUp(self):
        self.statement = Statement(text='A test statement.')

    def test_serializer(self):
        data = self.statement.serialize()
        self.assertEqual(self.statement.text, data['text'])
