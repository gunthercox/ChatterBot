from unittest import TestCase
from chatterbot.adapters.output import Gitter
from requests import Response
from mock import MagicMock


class GitterAdapterTestCase(TestCase):

    def setUp(self):
        super(GitterAdapterTestCase, self).setUp()
        self.adapter = Gitter()

    def test_validate_response_200(self):
        # Mock the response object
        response = Response()
        response.status_code = MagicMock(return_value=200)

        try:
            self.adatper._validate_response(response)
        except Exception:
            self.fail('Test raised exception unexpectedly!')

    def test_validate_response_201(self):
        # Mock the response object
        response = Response()
        response.status_code = MagicMock(return_value=201)

        try:
            self.adatper._validate_response(response)
        except Exception:
            self.fail('Test raised exception unexpectedly!')

    def test_response_status_code_not_ok(self):
        # Mock the response object
        response = Response()
        response.status_code = MagicMock(return_value=404)
        with self.assertRaises(Exception):
            self.adatper._validate_response(response)
