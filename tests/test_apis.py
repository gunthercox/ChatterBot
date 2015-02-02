# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase


class CleanFuncTests(ChatBotTestCase):

    def setUp(self):
        super(CleanFuncTests, self).setUp()

        from chatterbot.apis import clean
        self.clean = clean

    def test_linebreaks_removed(self):

        text = '\tThe quick \nbrown fox \rjumps over \vthe \alazy \fdog\\.'
        clean_text = self.clean(text)
        normal_text = 'The quick brown fox jumps over \vthe \alazy \fdog\\.'

        self.assertEqual(clean_text, normal_text)

    def test_leading_or_trailing_whitespace_removed(self):

        text = '     The quick brown fox jumps over the lazy dog.   '
        clean_text = self.clean(text)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(clean_text, normal_text)

    def test_consecutive_spaces_removed(self):

        text = 'The       quick brown     fox      jumps over the lazy dog.'
        clean_text = self.clean(text)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(clean_text, normal_text)

    def test_html_characters_restored(self):

        # implicit concat
        text = 'The quick brown fox &lt;b&gt;jumps&lt;/b&gt; over'
        ' the <a href="http://lazy.com">lazy</a> dog.'

        normal_text = 'The quick brown fox <b>jumps</b> over'
        ' the <a href="http://lazy.com">lazy</a> dog.'

        clean_text = self.clean(text)

        self.assertEqual(clean_text, normal_text)

    def test_non_ascii_chars_removed(self):

        text = u"Klüft skräms inför på fédéral électoral große"
        clean_text = self.clean(text)
        normal_text = "Kluft skrams infor pa federal electoral groe"

        self.assertEqual(clean_text, normal_text)
