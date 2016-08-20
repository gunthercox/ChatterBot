from tests.base_case import ChatBotTestCase
from .base import StorageIntegrationTests
from chatterbot.adapters.storage import JsonFileStorageAdapter


class JsonStorageIntegrationTests(StorageIntegrationTests, ChatBotTestCase):

    def setUp(self):
        super(JsonStorageIntegrationTests, self).setUp()

        self.chatbot.storage_adapters = []
        self.chatbot.storage = JsonFileStorageAdapter()
