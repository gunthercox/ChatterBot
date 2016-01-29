from unittest import TestCase
from chatterbot.adapters import Adaptation


class AdaptationTests(TestCase):

    def setUp(self):
        self.adaptation = Adaptation()

    def test_add_storage_adapter(self):
        self.adaptation.add_adapter(
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )
        self.assertEqual(len(self.adaptation.storage_adapters), 1)

    def test_add_logic_adapter(self):
        count_before = len(self.adaptation.logic.adapters)

        self.adaptation.add_adapter(
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )
        self.assertEqual(len(self.adaptation.logic.adapters), count_before + 1)

    def test_add_io_adapter(self):
        count_before = len(self.adaptation.io.adapters)

        self.adaptation.add_adapter(
            "chatterbot.adapters.io.TerminalAdapter"
        )
        self.assertEqual(len(self.adaptation.io.adapters), count_before + 1)
