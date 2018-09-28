# -*- coding: utf-8 -*-
from tests.base_case import ChatBotTestCase
from chatterbot.logic import LogicAdapter
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

    def test_response_with_tags_added(self):
        """
        If an input statement has tags added to it,
        that data should saved with the input statement.
        """
        self.test_statement.add_tags('test')
        self.chatbot.get_response(
            self.test_statement
        )

        results = self.chatbot.storage.filter(text=self.test_statement.text)

        self.assertIsLength(results, 1)
        self.assertIn('test', results[0].get_tags())

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

    def test_get_latest_response_from_zero_responses(self):
        response = self.chatbot.get_latest_response('invalid')

        self.assertIsNone(response)

    def test_get_latest_response_from_one_responses(self):
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')

        response = self.chatbot.get_latest_response('test')

        self.assertEqual(response.text, 'A')

    def test_get_latest_response_from_two_responses(self):
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')
        self.chatbot.storage.create(text='C', conversation='test', in_response_to='B')

        response = self.chatbot.get_latest_response('test')

        self.assertEqual(response.text, 'B')

    def test_get_latest_response_from_three_responses(self):
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')
        self.chatbot.storage.create(text='C', conversation='test', in_response_to='B')
        self.chatbot.storage.create(text='D', conversation='test', in_response_to='C')

        response = self.chatbot.get_latest_response('test')

        self.assertEqual(response.text, 'C')


class TestAdapterA(LogicAdapter):

    def process(self, statement):
        response = Statement('Good morning.')
        response.confidence = 0.2
        return response


class TestAdapterB(LogicAdapter):

    def process(self, statement):
        response = Statement('Good morning.')
        response.confidence = 0.5
        return response


class TestAdapterC(LogicAdapter):

    def process(self, statement):
        response = Statement('Good night.')
        response.confidence = 0.7
        return response


class ChatBotLogicAdapterTestCase(ChatBotTestCase):

    def test_sub_adapter_agreement(self):
        """
        In the case that multiple adapters agree on a given
        statement, this statement should be returned with the
        highest confidence available from these matching options.
        """
        self.chatbot.logic_adapters = [
            TestAdapterA(self.chatbot),
            TestAdapterB(self.chatbot),
            TestAdapterC(self.chatbot)
        ]

        statement = self.chatbot.generate_response(Statement('Howdy!'))

        self.assertEqual(statement.confidence, 0.5)
        self.assertEqual(statement, 'Good morning.')

    def test_get_logic_adapters(self):
        """
        Test that all system logic adapters and regular logic adapters
        can be retrieved as a list by a single method.
        """
        adapter_a = TestAdapterA(self.chatbot)
        adapter_b = TestAdapterB(self.chatbot)
        self.chatbot.system_logic_adapters = [adapter_a]
        self.chatbot.logic_adapters = [adapter_b]

        self.assertIsLength(self.chatbot.get_logic_adapters(), 2)
        self.assertIn(adapter_a, self.chatbot.get_logic_adapters())
        self.assertIn(adapter_b, self.chatbot.get_logic_adapters())

    def test_chatbot_set_for_all_logic_adapters(self):
        for sub_adapter in self.chatbot.get_logic_adapters():
            self.assertEqual(sub_adapter.chatbot, self.chatbot)
