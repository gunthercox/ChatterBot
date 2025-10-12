from chatterbot import ChatBot
from django.test import TransactionTestCase
from tests.django_integration import test_settings


class ChatterBotTestCase(TransactionTestCase):

    def setUp(self):
        super().setUp()
        self.chatbot = ChatBot(**test_settings.CHATTERBOT)

    def _create_with_search_text(self, text, in_response_to=None, **kwargs):
        """
        Helper function to create a statement with the search text populated.
        """
        search_in_response_to = None

        if in_response_to:
            search_in_response_to = self.chatbot.tagger.get_text_index_string(
                in_response_to
            )

        return self.chatbot.storage.create(
            text=text,
            in_response_to=in_response_to,
            search_text=self.chatbot.tagger.get_text_index_string(text),
            search_in_response_to=search_in_response_to,
            **kwargs
        )

    def _create_many_with_search_text(self, statements):
        """
        Helper function to bulk-create statements with the search text populated.
        """
        modified_statements = []

        for statement in statements:
            statement.search_text = self.chatbot.tagger.get_text_index_string(
                statement.text
            )

            if statement.in_response_to:
                statement.search_in_response_to = self.chatbot.tagger.get_text_index_string(
                    statement.in_response_to
                )

            modified_statements.append(statement)

        self.chatbot.storage.create_many(statements)
