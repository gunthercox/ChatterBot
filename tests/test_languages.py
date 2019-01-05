import sys
import inspect
from chatterbot import languages
from unittest import TestCase


class LanguageClassTests(TestCase):

    def test_classes_have_correct_attributes(self):
        language_classes = inspect.getmembers(sys.modules[languages.__name__])

        for name, obj in language_classes:
            if inspect.isclass(obj):
                self.assertTrue(hasattr(obj, 'ISO_639'))
                self.assertTrue(hasattr(obj, 'ENGLISH_NAME'))
                self.assertEqual(name, obj.ISO_639.upper())

        self.assertEqual(len(language_classes), 408)
