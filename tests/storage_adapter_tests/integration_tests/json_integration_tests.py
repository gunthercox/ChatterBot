from tests.base_case import ChatBotTestCase
from .base import StorageIntegrationTests


class JsonStorageIntegrationTests(StorageIntegrationTests, ChatBotTestCase):

    def setUp(self):
        super(JsonStorageIntegrationTests, self).setUp()

        self.chatbot.storage_adapters = []
        self.chatbot.add_adapter(
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )
