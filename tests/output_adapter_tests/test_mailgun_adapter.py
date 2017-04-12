from unittest import TestCase
from chatterbot.output import Mailgun


class MailgunAdapterTestCase(TestCase):

    def setUp(self):
        super(MailgunAdapterTestCase, self).setUp()
        self.adapter = Mailgun()
