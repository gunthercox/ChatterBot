from unittest import SkipTest
from tests.base_case import ChatBotTestCase
from .base import StorageIntegrationTests


class MongoStorageIntegrationTests(StorageIntegrationTests, ChatBotTestCase):

    def setUp(self):
        super(MongoStorageIntegrationTests, self).setUp()

        from pymongo.errors import ServerSelectionTimeoutError
        from pymongo import MongoClient

        # Skip these tests if a mongo client is not running
        try:
            client = MongoClient(
                serverSelectionTimeoutMS=0.5
            )
            client.server_info()

        except ServerSelectionTimeoutError:
            raise SkipTest("Unable to connect to mongo database.")

        self.chatbot.storage_adapters = []
        self.chatbot.add_adapter(
            "chatterbot.adapters.storage.MongoDatabaseAdapter"
        )
