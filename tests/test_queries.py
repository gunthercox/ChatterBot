from unittest import TestCase


class MongoAdapterTestCase(TestCase):

    def setUp(self):
        from chatterbot.storage.mongodb import Query
        self.query = Query()

    def test_statement_text_equals(self):
        query = self.query.statement_text_equals('Testing in progress')

        self.assertIn('text', query.value())
        self.assertEqual(query.value()['text'], 'Testing in progress')

    def test_statement_text_not_in(self):
        query = self.query.statement_text_not_in(['One', 'Two'])

        self.assertIn('text', query.value())
        self.assertIn('$nin', query.value()['text'])
        self.assertIn('One', query.value()['text']['$nin'])
        self.assertIn('Two', query.value()['text']['$nin'])

    def test_statement_response_list_contains(self):
        query = self.query.statement_response_list_contains('Hey')

        self.assertIn('in_response_to', query.value())
        self.assertIn('$elemMatch', query.value()['in_response_to'])
        self.assertIn('text', query.value()['in_response_to']['$elemMatch'])
        self.assertEqual('Hey', query.value()['in_response_to']['$elemMatch']['text'])

    def test_statement_response_list_equals(self):
        query = self.query.statement_response_list_equals([])

        self.assertIn('in_response_to', query.value())
        self.assertEqual(query.value()['in_response_to'], [])

    def test_raw(self):
        query = self.query.raw({'text': 'testing'})

        self.assertIn('text', query.value())
        self.assertEqual(query.value()['text'], 'testing')
