from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.logic import MultiLogicAdapter


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


class MultiLogicAdapterTestCase(ChatBotTestCase):

    def setUp(self):
        super(MultiLogicAdapterTestCase, self).setUp()
        self.adapter = MultiLogicAdapter()
        self.adapter.set_chatbot(self.chatbot)

    def test_sub_adapter_agreement(self):
        """
        In the case that multiple adapters agree on a given
        statement, this statement should be returned with the
        highest confidence available from these matching options.
        """
        self.adapter.add_adapter('tests.logic_adapter_tests.test_multi_adapter.TestAdapterA')
        self.adapter.add_adapter('tests.logic_adapter_tests.test_multi_adapter.TestAdapterB')
        self.adapter.add_adapter('tests.logic_adapter_tests.test_multi_adapter.TestAdapterC')

        statement = self.adapter.process(Statement('Howdy!'))

        self.assertEqual(statement.confidence, 0.5)
        self.assertEqual(statement, 'Good morning.')

    def test_get_greatest_confidence(self):
        statement = 'Hello'
        options = [
            (0.50, 'Hello'),
            (0.85, 'Hello'),
            (0.42, 'Hello')
        ]
        value = self.adapter.get_greatest_confidence(statement, options)

        self.assertEqual(value, 0.85)

    def test_add_adapter(self):
        adapter_count_before = len(self.adapter.adapters)
        self.adapter.add_adapter('tests.logic_adapter_tests.test_multi_adapter.TestAdapterA')
        adapter_count_after = len(self.adapter.adapters)

        self.assertEqual(adapter_count_after, adapter_count_before + 1)

    def test_get_adapters(self):
        """
        TODO
        """
        import unittest
        raise unittest.SkipTest('This test needs to be written.')

    def test_get_initialization_functions(self):
        """
        TODO
        """
        import unittest
        raise unittest.SkipTest('This test needs to be written.')

    def test_insert_logic_adapter(self):
        """
        TODO
        """
        import unittest
        raise unittest.SkipTest('This test needs to be written.')

    def test_remove_logic_adapter(self):
        """
        TODO
        """
        import unittest
        raise unittest.SkipTest('This test needs to be written.')

    def test_set_chatbot(self):
        adapter = MultiLogicAdapter()
        adapter.set_chatbot(self.chatbot)

        # Test that the multi adapter has acccess to the chat bot
        self.assertEqual(adapter.chatbot, self.chatbot)

        # Test that all sub adapters have the chatbot set
        for sub_adapter in adapter.adapters:
            self.assertEqual(sub_adapter.chatbot, self.chatbot)
