from django.test import TestCase
from django.utils import timezone
from chatterbot.conversation import Statement as StatementObject
from chatterbot.ext.django_chatterbot.models import Statement as StatementModel


class StatementIntegrationTestCase(TestCase):
    """
    Test case to make sure that the Django Statement model
    and ChatterBot Statement object have a common interface.
    """

    def setUp(self):
        super(StatementIntegrationTestCase, self).setUp()
        date_created = timezone.now()
        self.object = StatementObject(text='_', created_at=date_created)
        self.model = StatementModel(text='_', created_at=date_created)

    def test_text(self):
        self.assertTrue(hasattr(self.object, 'text'))
        self.assertTrue(hasattr(self.model, 'text'))

    def test_in_response_to(self):
        self.assertTrue(hasattr(self.object, 'in_response_to'))
        self.assertTrue(hasattr(self.model, 'in_response_to'))

    def test_extra_data(self):
        self.assertTrue(hasattr(self.object, 'extra_data'))
        self.assertTrue(hasattr(self.model, 'extra_data'))

    def test__str__(self):
        self.assertTrue(hasattr(self.object, '__str__'))
        self.assertTrue(hasattr(self.model, '__str__'))

        self.assertEqual(str(self.object), str(self.model))

    def test_add_extra_data(self):
        self.object.add_extra_data('key', 'value')
        self.model.add_extra_data('key', 'value')

    def test_serialize(self):
        object_data = self.object.serialize()
        model_data = self.model.serialize()

        object_data_created_at = object_data.pop('created_at')
        model_data_created_at = model_data.pop('created_at')

        self.assertEqual(object_data, model_data)
        self.assertEqual(object_data_created_at.date(), model_data_created_at.date())

    def test_response_statement_cache(self):
        self.assertTrue(hasattr(self.object, 'response_statement_cache'))
        self.assertTrue(hasattr(self.model, 'response_statement_cache'))
