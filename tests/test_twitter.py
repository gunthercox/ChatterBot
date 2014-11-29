from .base_case import ChatBotTestCase
from chatterbot.algorithms.twitter import remove_leeding_usernames
from chatterbot.algorithms.twitter import remove_trailing_usernames


class TwitterTests(ChatBotTestCase):

    def test_remove_leeding_usernames(self):

        string = "@CERN @Space Happy black friday! Keep hunting for black holes! @NASA"
        string = remove_leeding_usernames(string)
        result = "Happy black friday! Keep hunting for black holes! @NASA"

        self.assertEqual(string, result)

    def test_remove_trailing_usernames(self):

        string = "@ASIMO Watch your step @Demo @in @Tokyo"
        string = remove_trailing_usernames(string)
        result = "@ASIMO Watch your step"

        self.assertEqual(string, result)
