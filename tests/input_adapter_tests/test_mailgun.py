from unittest import TestCase
from chatterbot.adapters.input import Mailgun


class MailgunAdapterTests(TestCase):

    def setUp(self):
        super(MailgunAdapterTests, self).setUp()
        self.adapter = Mailgun()