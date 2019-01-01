from tests_django.base_case import ChatterBotTestCase
from chatterbot.conversation import Statement


class LogicIntegrationTestCase(ChatterBotTestCase):
    """
    Tests to make sure that logic adapters
    function correctly when using Django.
    """

    def setUp(self):
        super().setUp()

        self.chatbot.storage.create(text='Default statement')

    def test_best_match(self):
        from chatterbot.logic import BestMatch

        adapter = BestMatch(self.chatbot)

        statement1 = self.chatbot.storage.create(
            text='Do you like programming?',
            conversation='test'
        )

        self.chatbot.storage.create(
            text='Yes',
            in_response_to=statement1.text,
            conversation='test'
        )

        response = adapter.process(statement1)

        self.assertEqual(response.text, 'Yes')
        self.assertEqual(response.confidence, 1)

    def test_mathematical_evaluation(self):
        from chatterbot.logic import MathematicalEvaluation

        adapter = MathematicalEvaluation(self.chatbot)

        statement = Statement(text='What is 6 + 6?')

        response = adapter.process(statement)

        self.assertEqual(response.text, '6 + 6 = 12')
        self.assertEqual(response.confidence, 1)

    def test_time(self):
        from chatterbot.logic import TimeLogicAdapter

        adapter = TimeLogicAdapter(self.chatbot)

        statement = Statement(text='What time is it?')

        response = adapter.process(statement)

        self.assertIn('The current time is', response.text)
        self.assertEqual(response.confidence, 1)
