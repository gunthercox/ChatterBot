from django.test import TestCase
from chatterbot.conversation import Statement as StatementObject
from chatterbot.ext.django_chatterbot.models import Statement as StatementModel


class StatementIntegrationTestCase(TestCase):
    """
    Test case to make sure that the Django Statement model
    and ChatterBot Statement object have a common interface.
    """

    def setUp(self):
        super(StatementIntegrationTestCase, self).setUp()

        from datetime import datetime
        from pytz import UTC

        now = datetime(2020, 2, 15, 3, 14, 10, 0, UTC)

        self.object = StatementObject(text='_', created_at=now)
        self.model = StatementModel(text='_', created_at=now)

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

        self.assertEqual(object_data, model_data)
