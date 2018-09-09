# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement


class ChatterBotResponseTestCase(ChatBotTestCase):

    def setUp(self):
        super(ChatterBotResponseTestCase, self).setUp()

        self.test_statement = Statement('Hello', in_response_to='Hi')

    def test_empty_database(self):
        """
        If there is no statements in the database, then the
        user's input is the only thing that can be returned.
        """
        response = self.chatbot.get_response('How are you?')

        self.assertEqual('How are you?', response)

    def test_statement_saved_empty_database(self):
        """
        Test that when database is empty, the first
        statement is saved and returned as a response.
        """
        statement_text = 'Wow!'
        response = self.chatbot.get_response(statement_text)

        results = self.chatbot.storage.filter(text=statement_text)

        self.assertIsLength(results, 1)
        self.assertEqual(response, statement_text)

    def test_statement_added_to_conversation(self):
        """
        An input statement should be added to the recent response list.
        """
        statement = Statement(text='Wow!', conversation='test')
        response = self.chatbot.get_response(statement)

        self.assertEqual(statement.text, response)
        self.assertEqual(response.conversation, 'test')

    def test_response_known(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')

        self.assertEqual(response, self.test_statement.text)

    def test_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')
        results = self.chatbot.storage.filter(text=response.text)

        self.assertEqual(response, self.test_statement.text)
        self.assertIsLength(results, 1)
        self.assertEqual(results[0].in_response_to, 'Hi')

    def test_second_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')
        self.assertEqual(response.text, 'Hello')

        second_response = self.chatbot.get_response('How are you?')
        results = self.chatbot.storage.filter(text=second_response.text)

        # Make sure that the second response was saved to the database
        self.assertIsLength(self.chatbot.storage.filter(text='How are you?'), 1)

        self.assertEqual(second_response, self.test_statement.text)
        self.assertIsLength(results, 1)
        self.assertEqual(results[0].in_response_to, 'Hi')

    def test_get_response_unicode(self):
        """
        Test the case that a unicode string is passed in.
        """
        response = self.chatbot.get_response(u'سلام')
        self.assertGreater(len(response.text), 0)

    def test_get_response_emoji(self):
        """
        Test the case that the input string contains an emoji.
        """
        response = self.chatbot.get_response(u'💩 ')
        self.assertGreater(len(response.text), 0)

    def test_get_response_non_whitespace(self):
        """
        Test the case that a non-whitespace C1 control string is passed in.
        """
        response = self.chatbot.get_response(u'')
        self.assertGreater(len(response.text), 0)

    def test_get_response_two_byte_characters(self):
        """
        Test the case that a string containing two-byte characters is passed in.
        """
        response = self.chatbot.get_response(u'田中さんにあげて下さい')
        self.assertGreater(len(response.text), 0)

    def test_get_response_corrupted_text(self):
        """
        Test the case that a string contains "corrupted" text.
        """
        response = self.chatbot.get_response(u'Ṱ̺̺̕h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳.̨̹͈̣')
        self.assertGreater(len(response.text), 0)

    def test_response_extra_data(self):
        """
        If an input statement has data contained in the
        `extra_data` attribute of a statement object,
        that data should saved with the input statement.
        """
        self.test_statement.add_extra_data('test', 1)
        self.chatbot.get_response(
            self.test_statement
        )

        results = self.chatbot.storage.filter(text=self.test_statement.text)

        self.assertIsLength(results, 1)
        self.assertIn('test', results[0].extra_data)
        self.assertEqual(1, results[0].extra_data['test'])

    def test_generate_response(self):
        statement = Statement('Many insects adopt a tripedal gait for rapid yet stable walking.')
        response = self.chatbot.generate_response(statement)

        self.assertEqual(response, statement)
        self.assertEqual(response.confidence, 1)

    def test_learn_response(self):
        previous_response = Statement('Define Hemoglobin.')
        statement = Statement('Hemoglobin is an oxygen-transport metalloprotein.')
        self.chatbot.learn_response(statement, previous_response)
        results = self.chatbot.storage.filter(text=statement.text)

        self.assertIsLength(results, 1)

    def test_get_response_does_not_add_new_statement(self):
        """
        Test that a new statement is not learned if `read_only` is set to True.
        """
        self.chatbot.read_only = True
        self.chatbot.get_response('Hi!')
        results = self.chatbot.storage.filter(text='Hi!')

        self.assertIsLength(results, 0)
