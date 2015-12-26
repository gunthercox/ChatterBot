from unittest import TestCase
from chatterbot.adapters import Adaptation


class AdaptationTests(TestCase):

    def setUp(self):
        self.adaptation = Adaptation()

    def test_add_adapter(self):
        self.adaptation.add_adapter(
            "storage",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )
        self.assertTrue(hasattr(self.adaptation.context, "storage"))

    def test_context_can_be_set(self):
        self.adaptation.context.name = "ChatterBot"
        self.assertEqual(self.adaptation.context.name, "ChatterBot")

