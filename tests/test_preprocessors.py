# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot import preprocessors


class PreprocessorIntegrationTestCase(ChatBotTestCase):
    """
    Make sure that preprocessors work with the chat bot.
    """

    def test_clean_whitespace(self):
        self.chatbot.preprocessors = [preprocessors.clean_whitespace]
        response = self.chatbot.get_response('Hello,    how are you?')

        self.assertEqual(response.text, 'Hello, how are you?')


class CleanWhitespacePreprocessorTestCase(ChatBotTestCase):
    """
    Make sure that ChatterBot's whitespace removing preprocessor works as expected.
    """

    def test_clean_whitespace(self):
        statement = Statement('\tThe quick \nbrown fox \rjumps over \vthe \alazy \fdog\\.')
        cleaned = preprocessors.clean_whitespace(self.chatbot, statement)
        normal_text = 'The quick brown fox jumps over \vthe \alazy \fdog\\.'

        self.assertEqual(cleaned.text, normal_text)

    def test_leading_or_trailing_whitespace_removed(self):
        statement = Statement('     The quick brown fox jumps over the lazy dog.   ')
        cleaned = preprocessors.clean_whitespace(self.chatbot, statement)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(cleaned.text, normal_text)

    def test_consecutive_spaces_removed(self):
        statement = Statement('The       quick brown     fox      jumps over the lazy dog.')
        cleaned = preprocessors.clean_whitespace(self.chatbot, statement)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(cleaned.text, normal_text)


class HTMLUnescapePreprocessorTestCase(ChatBotTestCase):
    """
    Make sure that ChatterBot's html unescaping preprocessor works as expected.
    """

    def test_html_unescape(self):

        # implicit concatenation
        statement = Statement(
            'The quick brown fox &lt;b&gt;jumps&lt;/b&gt; over'
            ' the <a href="http://lazy.com">lazy</a> dog.'
        )

        normal_text = (
            'The quick brown fox <b>jumps</b> over'
            ' the <a href="http://lazy.com">lazy</a> dog.'
        )

        cleaned = preprocessors.unescape_html(self.chatbot, statement)

        self.assertEqual(cleaned.text, normal_text)


class ConvertToASCIIPreprocessorTestCase(ChatBotTestCase):
    """
    Make sure that ChatterBot's ASCII conversion preprocessor works as expected.
    """

    def test_convert_to_ascii(self):
        statement = Statement(u'Klüft skräms inför på fédéral électoral große')
        cleaned = preprocessors.convert_to_ascii(self.chatbot, statement)
        normal_text = 'Kluft skrams infor pa federal electoral groe'

        self.assertEqual(cleaned.text, normal_text)
