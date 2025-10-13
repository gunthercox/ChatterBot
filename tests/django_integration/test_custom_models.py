"""
Tests for custom model swapping functionality.
"""
from tests.django_integration.base_case import ChatterBotTestCase
from django.test import override_settings
from chatterbot import ChatBot


class CustomModelsTestCase(ChatterBotTestCase):
    """
    Test custom model configuration via settings and kwargs.
    """

    def test_default_models_used_without_settings(self):
        """
        Test that default models are used when no custom settings provided.
        """
        chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter'
        )

        # Should use default django_chatterbot.Statement model
        self.assertEqual(
            chatbot.storage.statement_model,
            'django_chatterbot.Statement'
        )
        self.assertEqual(
            chatbot.storage.tag_model,
            'django_chatterbot.Tag'
        )

    def test_custom_models_via_kwargs(self):
        """
        Test that custom models can be specified via kwargs.
        """
        chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter',
            statement_model='myapp.CustomStatement',
            tag_model='myapp.CustomTag'
        )

        self.assertEqual(chatbot.storage.statement_model, 'myapp.CustomStatement')
        self.assertEqual(chatbot.storage.tag_model, 'myapp.CustomTag')

    @override_settings(
        CHATTERBOT_STATEMENT_MODEL='myapp.CustomStatement',
        CHATTERBOT_TAG_MODEL='myapp.CustomTag'
    )
    def test_custom_models_via_settings(self):
        """
        Test that custom models can be specified via Django settings.
        """
        chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter'
        )

        # Should read from Django settings
        self.assertEqual(chatbot.storage.statement_model, 'myapp.CustomStatement')
        self.assertEqual(chatbot.storage.tag_model, 'myapp.CustomTag')

    def test_kwargs_override_settings(self):
        """
        Test that kwargs take precedence over Django settings.
        """
        with override_settings(
            CHATTERBOT_STATEMENT_MODEL='settings.StatementModel',
            CHATTERBOT_TAG_MODEL='settings.TagModel'
        ):
            chatbot = ChatBot(
                'Test Bot',
                storage_adapter='chatterbot.storage.DjangoStorageAdapter',
                statement_model='kwargs.StatementModel',
                tag_model='kwargs.TagModel'
            )

            # kwargs should take precedence over settings
            self.assertEqual(chatbot.storage.statement_model, 'kwargs.StatementModel')
            self.assertEqual(chatbot.storage.tag_model, 'kwargs.TagModel')

    def test_get_statement_model(self):
        """
        Test that get_statement_model() returns the correct model class.
        """
        chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter'
        )

        Statement = chatbot.storage.get_statement_model()

        # Should be the default Statement model
        self.assertEqual(Statement.__name__, 'Statement')
        self.assertEqual(Statement._meta.app_label, 'django_chatterbot')

    def test_get_tag_model(self):
        """
        Test that get_tag_model() returns the correct model class.
        """
        chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter'
        )

        Tag = chatbot.storage.get_tag_model()

        # Should be the default Tag model
        self.assertEqual(Tag.__name__, 'Tag')
        self.assertEqual(Tag._meta.app_label, 'django_chatterbot')

    def test_model_configuration_persists(self):
        """
        Test that model configuration is stored correctly on the adapter instance.
        """
        chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter',
            statement_model='app1.Model1',
            tag_model='app2.Model2'
        )

        # Configuration should persist
        self.assertEqual(chatbot.storage.statement_model, 'app1.Model1')
        self.assertEqual(chatbot.storage.tag_model, 'app2.Model2')

        # Should be the same after multiple accesses
        self.assertEqual(chatbot.storage.statement_model, 'app1.Model1')
        self.assertEqual(chatbot.storage.tag_model, 'app2.Model2')
