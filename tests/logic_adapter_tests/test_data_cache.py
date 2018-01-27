from tests.base_case import ChatBotTestCase
from chatterbot.logic import LogicAdapter
from chatterbot.trainers import ListTrainer


class DummyMutatorLogicAdapter(LogicAdapter):
    """
    This is a dummy class designed to modify a
    the resulting statement before it is returned.
    """

    def process(self, statement):
        statement.add_extra_data('pos_tags', 'NN')

        self.chatbot.storage.update(statement)
        statement.confidence = 1
        return statement


class DataCachingTests(ChatBotTestCase):

    def setUp(self):
        super(DataCachingTests, self).setUp()

        self.chatbot.logic = DummyMutatorLogicAdapter()
        self.chatbot.logic.set_chatbot(self.chatbot)

        self.chatbot.set_trainer(ListTrainer, **self.get_kwargs())

        self.chatbot.train([
            'Hello',
            'How are you?'
        ])

    def test_additional_attributes_saved(self):
        """
        Test that an additional data attribute can be added to the statement
        and that this attribute is saved.
        """
        self.chatbot.get_response('Hello')
        found_statement = self.chatbot.storage.find('Hello')
        data = found_statement.serialize()

        self.assertIsNotNone(found_statement)
        self.assertIn('extra_data', data)
        self.assertIn('pos_tags', data['extra_data'])
        self.assertEqual('NN', data['extra_data']['pos_tags'])
