from unittest import TestCase, expectedFailure


class TuringTests(TestCase):

    def setUp(self):
        from chatterbot import ChatBot

        self.chatbot = ChatBot('Agent Jr.')

    @expectedFailure
    def test_ask_name(self):
        response = self.chatbot.get_response(
            'What is your name?'
        )
        self.assertIn('Agent', response.text)

    @expectedFailure
    def test_repeat_information(self):
        """
        Test if we can detect any repeated responses from the agent.
        """
        self.fail('Condition not met.')

    @expectedFailure
    def test_repeat_input(self):
        """
        Test what the responses are like, if we keep giving the same input.
        """
        self.fail('Condition not met.')

    @expectedFailure
    def test_contradicting_responses(self):
        """
        Test if we can get the agent to contradict itself.
        """
        self.fail('Condition not met.')

    @expectedFailure
    def test_mathematical_ability(self):
        """
        The math questions inherently suggest that the agent
        should get some math problems wrong in order to seem
        more human. My view on this is that it is more useful
        to have a bot which is good at math and it could solve
        it like a normal human being.
        """
        self.fail('Condition not met.')

    @expectedFailure
    def test_response_time(self):
        """
        Does the agent respond in a realistic amount of time?
        """
        self.fail('Condition not met.')
