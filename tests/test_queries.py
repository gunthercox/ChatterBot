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

    def test_raw(self):
        query = self.query.raw({'text': 'testing'})

        self.assertIn('text', query.value())
        self.assertEqual(query.value()['text'], 'testing')
