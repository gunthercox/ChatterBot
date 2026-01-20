from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot import preprocessors_greek

class PreprocessorFixFinalSigmaTestCase(ChatBotTestCase):
    """
    Make sure ChatterBot's final sigma replacing preprocessor works as expected.
    """

    def test_fix_final_sigma(self):
        statement = Statement(text='Γεια σασ')

        fixed = preprocessors_greek.fix_final_sigma(statement)
        normalText = 'Γεια σας'
        self.chatbot.preprocessors = [preprocessors.clean_whitespace]

        self.assertEqual(fixed.text, normalText)
