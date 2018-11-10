from unittest import TestCase
from chatterbot.output import Mailgun


class MailgunAdapterTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.adapter = Mailgun()
