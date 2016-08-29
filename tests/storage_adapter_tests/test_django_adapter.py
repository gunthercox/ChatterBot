from unittest import TestCase
from chatterbot.adapters.storage import DjangoStorageAdapter
from chatterbot.conversation import Statement, Response


class BaseDjangoStorageAdapterTestCase(TestCase):

    def setUp(self):
        self.adapter = DjangoStorageAdapter()

