from unittest import TestCase


class MongoAdapterTestCase(TestCase):

    def setUp(self):
        from chatterbot.storage.mongodb import Query
        self.query = Query()

    def test_statement_in_response_to_not_in(self):
        query = self.query.statement_in_response_to_not_in(['One', 'Two'])

        self.assertIn('in_response_to', query.value())
        self.assertIn('$nin', query.value()['in_response_to'])
        self.assertIn('One', query.value()['in_response_to']['$nin'])
        self.assertIn('Two', query.value()['in_response_to']['$nin'])

    def test_raw(self):
        query = self.query.raw({'text': 'testing'})

        self.assertIn('text', query.value())
        self.assertEqual(query.value()['text'], 'testing')
