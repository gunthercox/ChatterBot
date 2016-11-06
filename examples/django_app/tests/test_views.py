from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from chatterbot.ext.django_chatterbot.views import ChatterBotView, ChatterBotTrainingView


class ChatterBotViewTestCase(TestCase):

    def setUp(self):
        super(ChatterBotViewTestCase, self).setUp()
        self.view = ChatterBotView()

    def test_validate_text(self):
        try:
            self.view.validate({
                'text': 'How are you?'
            })
        except ValidationError:
            self.fail('Test raised ValidationError unexpectedly!')

    def test_validate_invalid_text(self):
        with self.assertRaises(ValidationError):
            self.view.validate({
                'type': 'classmethod'
            })


class TrainingViewTestCase(TestCase):

    def setUp(self):
        super(TrainingViewTestCase, self).setUp()
        self.view = ChatterBotTrainingView()
        self.training_endpoint = reverse('chatterbot:train')

    def test_invalid_training_data(self):
        training_data = {
            'conversation': [
                'How are you?',
                'I am good'
            ]
        }

    def test_valid_training_data(self):
        training_data = {
            'conversation': [
                {'text': 'I am good', 'in_response_to': 'How are you?'}
            ]
        }