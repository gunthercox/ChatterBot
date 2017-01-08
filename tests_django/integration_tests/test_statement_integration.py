from django.test import TestCase
from django.utils import timezone
from chatterbot.conversation import Statement as StatementObject
from chatterbot.conversation import Response as ResponseObject
from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
from chatterbot.ext.django_chatterbot.models import Response as ResponseModel


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

    def test_add_response(self):
        self.assertTrue(hasattr(self.object, 'add_response'))
        self.assertTrue(hasattr(self.model, 'add_response'))

    def test_remove_response(self):
        self.object.add_response(ResponseObject('Hello'))
        model_response_statement = StatementModel.objects.create(text='Hello')
        self.model.save()
        self.model.in_response.create(statement=self.model, response=model_response_statement)

        object_removed = self.object.remove_response('Hello')
        model_removed = self.model.remove_response('Hello')

        self.assertTrue(object_removed)
        self.assertTrue(model_removed)

    def test_get_response_count(self):
        self.object.add_response(ResponseObject('Hello', occurrence=2))
        model_response_statement = StatementModel.objects.create(text='Hello')
        self.model.save()
        self.model.in_response.create(
            statement=self.model, response=model_response_statement, occurrence=2
        )

        object_count = self.object.get_response_count(StatementObject(text='Hello'))
        model_count = self.model.get_response_count(StatementModel(text='Hello'))

        self.assertEqual(object_count, 2)
        self.assertEqual(model_count, 2)

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


class ResponseIntegrationTestCase(TestCase):

    """
    Test case to make sure that the Django Response model
    and ChatterBot Response object have a common interface.
    """

    def setUp(self):
        super(ResponseIntegrationTestCase, self).setUp()
        date_created = timezone.now()
        statement_object = StatementObject(text='_', created_at=date_created)
        statement_model = StatementModel.objects.create(text='_', created_at=date_created)
        self.object = ResponseObject(statement_object.text)
        self.model = ResponseModel(statement=statement_model, response=statement_model)

    def test_serialize(self):
        object_data = self.object.serialize()
        model_data = self.model.serialize()

        self.assertEqual(object_data, model_data)
