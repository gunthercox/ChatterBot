import inspect
from chatterbot import languages
from unittest import TestCase


class LanguageClassTests(TestCase):

    def test_classes_have_correct_attributes(self):
        language_classes = languages.get_language_classes()

        for name, obj in language_classes:
            self.assertTrue(inspect.isclass(obj))
            self.assertTrue(hasattr(obj, 'ISO_639'))
            self.assertTrue(hasattr(obj, 'ISO_639_1'))
            self.assertTrue(hasattr(obj, 'ENGLISH_NAME'))
            self.assertEqual(name, obj.ISO_639.upper())

        self.assertEqual(len(language_classes), 402)
