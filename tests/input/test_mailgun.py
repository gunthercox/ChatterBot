from unittest import TestCase
from chatterbot.input import Mailgun


class MailgunAdapterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.adapter = Mailgun()
