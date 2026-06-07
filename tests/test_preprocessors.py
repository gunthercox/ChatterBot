from tests.base_case import ChatBotTestCase
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
        statement = Statement(text='\tThe quick \nbrown fox \rjumps over \vthe \alazy \fdog\\.')
        cleaned = preprocessors.clean_whitespace(statement)
        normal_text = 'The quick brown fox jumps over the \alazy dog\\.'

        self.assertEqual(cleaned.text, normal_text)

    def test_leading_or_trailing_whitespace_removed(self):
        statement = Statement(text='     The quick brown fox jumps over the lazy dog.   ')
        cleaned = preprocessors.clean_whitespace(statement)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(cleaned.text, normal_text)

    def test_consecutive_spaces_removed(self):
        statement = Statement(text='The       quick brown     fox      jumps over the lazy dog.')
        cleaned = preprocessors.clean_whitespace(statement)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(cleaned.text, normal_text)


class HTMLUnescapePreprocessorTestCase(ChatBotTestCase):
    """
    Make sure that ChatterBot's html unescaping preprocessor works as expected.
    """

    def test_html_unescape(self):

        # implicit concatenation
        statement = Statement(
            text=(
                'The quick brown fox &lt;b&gt;jumps&lt;/b&gt; over'
                ' the <a href="http://lazy.com">lazy</a> dog.'
            )
        )

        normal_text = (
            'The quick brown fox <b>jumps</b> over'
            ' the <a href="http://lazy.com">lazy</a> dog.'
        )

        cleaned = preprocessors.unescape_html(statement)

        self.assertEqual(cleaned.text, normal_text)


class ConvertToASCIIPreprocessorTestCase(ChatBotTestCase):
    """
    Make sure that ChatterBot's ASCII conversion preprocessor works as expected.
    """

    def test_convert_to_ascii(self):
        statement = Statement(text=u'Klüft skräms inför på fédéral électoral große')
        cleaned = preprocessors.convert_to_ascii(statement)
        normal_text = 'Kluft skrams infor pa federal electoral groe'

        self.assertEqual(cleaned.text, normal_text)
        
class NormalizeRepeatingCharactersPreprocessorTestCase(ChatBotTestCase):
    """
    Make sure that ChatterBot's repeating-character preprocessor works as expected.
    """

    def test_elongated_word_is_reduced(self):
        statement = Statement(text='I am sooooo happy')
        cleaned = preprocessors.normalize_repeating_characters(statement)
        self.assertEqual(cleaned.text, 'I am soo happy')

    def test_multiple_elongated_words(self):
        statement = Statement(text='Yesss that was greaaaat')
        cleaned = preprocessors.normalize_repeating_characters(statement)
        self.assertEqual(cleaned.text, 'Yess that was greaat')

    def test_natural_double_letters_preserved(self):
        statement = Statement(text='That book looks really cool')
        cleaned = preprocessors.normalize_repeating_characters(statement)
        self.assertEqual(cleaned.text, 'That book looks really cool')

    def test_repeating_digits_preserved(self):
        statement = Statement(text='I have 1000000 dollars')
        cleaned = preprocessors.normalize_repeating_characters(statement)
        self.assertEqual(cleaned.text, 'I have 1000000 dollars')

    def test_repeating_punctuation_preserved(self):
        statement = Statement(text='Wow!!!')
        cleaned = preprocessors.normalize_repeating_characters(statement)
        self.assertEqual(cleaned.text, 'Wow!!!')
