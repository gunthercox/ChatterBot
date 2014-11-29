# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase


class ChatBotApiTests(ChatBotTestCase):

    def test_clean_function(self):
        """
        Ensure that non-ascii characters are correctly removed
        """
        from chatterbot.apis import clean

        text = u"Klüft skräms inför på fédéral électoral große"
        clean_text = clean(text)
        normal_text = "Kluft skrams infor pa federal electoral groe"

        self.assertEqual(clean_text, normal_text)
