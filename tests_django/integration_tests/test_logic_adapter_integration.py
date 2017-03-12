from django.test import TestCase
from chatterbot.ext.django_chatterbot.models import Statement, Response


class LogicIntegrationTestCase(TestCase):
    """
    Tests to make sure that logic adapters
    function correctly when using Django.
    """

    def setUp(self):
        super(LogicIntegrationTestCase, self).setUp()
        from chatterbot import ChatBot
        from chatterbot.ext.django_chatterbot import settings

        self.chatbot = ChatBot(**settings.CHATTERBOT)

        Statement.objects.create(text='Default statement')

    def test_best_match(self):
        from chatterbot.logic import BestMatch

        adapter = BestMatch()
        adapter.set_chatbot(self.chatbot)

        statement1 = Statement(text='Do you like programming?')
        statement1.save()

        statement2 = Statement(text='Yes')
        statement2.save()

        response = Response(statement=statement1, response=statement2)
        response.save()

        response = adapter.process(statement1)

        self.assertEqual(response.text, 'Yes')
        self.assertEqual(response.confidence, 1)

    def test_low_confidence(self):
        from chatterbot.logic import LowConfidenceAdapter

        adapter = LowConfidenceAdapter()
        adapter.set_chatbot(self.chatbot)

        statement = Statement(text='Why is the sky blue?')

        response = adapter.process(statement)

        self.assertEqual(response.text, adapter.default_response)

    def test_mathematical_evaluation(self):
        from chatterbot.logic import MathematicalEvaluation

        adapter = MathematicalEvaluation()
        adapter.set_chatbot(self.chatbot)

        statement = Statement(text='What is 6 + 6?')

        response = adapter.process(statement)

        self.assertEqual(response.text, '( 6 + 6 ) = 12')
        self.assertEqual(response.confidence, 1)

    def test_time(self):
        from chatterbot.logic import TimeLogicAdapter

        adapter = TimeLogicAdapter()
        adapter.set_chatbot(self.chatbot)

        statement = Statement(text='What time is it?')

        response = adapter.process(statement)

        self.assertIn('The current time is', response.text)
        self.assertEqual(response.confidence, 1)
