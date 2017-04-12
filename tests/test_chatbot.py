# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement, Response


class ChatterBotResponseTestCase(ChatBotTestCase):

    def setUp(self):
        super(ChatterBotResponseTestCase, self).setUp()

        response_list = [
            Response('Hi')
        ]

        self.test_statement = Statement('Hello', in_response_to=response_list)

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

        saved_statement = self.chatbot.storage.find(statement_text)

        self.assertIsNotNone(saved_statement)
        self.assertEqual(response, statement_text)

    def test_statement_added_to_recent_response_list(self):
        """
        An input statement should be added to the recent response list.
        """
        statement_text = 'Wow!'
        response = self.chatbot.get_response(statement_text)
        session = self.chatbot.conversation_sessions.get(
            self.chatbot.default_session.id_string
        )

        self.assertIn(statement_text, session.conversation[0])
        self.assertEqual(response, statement_text)

    def test_response_known(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')

        self.assertEqual(response, self.test_statement.text)

    def test_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')
        statement_object = self.chatbot.storage.find(response.text)

        self.assertEqual(response, self.test_statement.text)
        self.assertIsLength(statement_object.in_response_to, 1)
        self.assertIn('Hi', statement_object.in_response_to)

    def test_second_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')
        # response = 'Hello'
        second_response = self.chatbot.get_response('How are you?')
        statement = self.chatbot.storage.find(second_response.text)

        # Make sure that the second response was saved to the database
        self.assertIsNotNone(self.chatbot.storage.find('How are you?'))

        self.assertEqual(second_response, self.test_statement.text)
        self.assertIsLength(statement.in_response_to, 1)
        self.assertIn('Hi', statement.in_response_to)

    def test_get_response_unicode(self):
        """
        Test the case that a unicode string is passed in.
        """
        response = self.chatbot.get_response(u'سلام')
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

        saved_statement = self.chatbot.storage.find(
            self.test_statement.text
        )

        self.assertIn('test', saved_statement.extra_data)
        self.assertEqual(1, saved_statement.extra_data['test'])

    def test_generate_response(self):
        statement = Statement('Many insects adopt a tripedal gait for rapid yet stable walking.')
        input_statement, response = self.chatbot.generate_response(
            statement,
            self.chatbot.default_session.id
        )

        self.assertEqual(input_statement, statement)
        self.assertEqual(response, statement)
        self.assertEqual(response.confidence, 1)

    def test_learn_response(self):
        previous_response = Statement('Define Hemoglobin.')
        statement = Statement('Hemoglobin is an oxygen-transport metalloprotein.')
        self.chatbot.learn_response(statement, previous_response)
        exists = self.chatbot.storage.find(statement.text)

        self.assertIsNotNone(exists)

    def test_update_does_not_add_new_statement(self):
        """
        Test that a new statement is not learned if `read_only` is set to True.
        """
        self.chatbot.read_only = True
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi!')
        statement_found = self.chatbot.storage.find('Hi!')

        self.assertEqual(response, self.test_statement.text)
        self.assertIsNone(statement_found)


class ChatBotConfigFileTestCase(ChatBotTestCase):

    def setUp(self):
        super(ChatBotConfigFileTestCase, self).setUp()
        import json
        self.config_file_path = './test-config.json'
        self.data = self.get_kwargs()
        self.data['name'] = 'Config Test'

        with open(self.config_file_path, 'w+') as config_file:
            json.dump(self.data, config_file)

    def tearDown(self):
        super(ChatBotConfigFileTestCase, self).tearDown()
        import os

        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

    def test_read_from_config_file(self):
        from chatterbot import ChatBot
        self.chatbot = ChatBot.from_config(self.config_file_path)

        self.assertEqual(self.chatbot.name, self.data['name'])
