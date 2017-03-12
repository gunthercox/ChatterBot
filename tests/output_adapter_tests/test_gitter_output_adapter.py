from unittest import TestCase
from mock import Mock
from chatterbot.conversation import Statement
from chatterbot.input import gitter
from chatterbot.output import Gitter


class MockResponse(object):

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


def mock_post_response(*args, **kwargs):
    url = args[0]
    data = kwargs.get('data', {})

    endpoints = {
        'https://api.gitter.im/v1/rooms': MockResponse(200, {'id': '40999743'}),
        'https://api.gitter.im/v1/rooms/40999743/chatMessages': MockResponse(200, {})
    }

    return endpoints.get(url)


class GitterAdapterTestCase(TestCase):

    def setUp(self):
        super(GitterAdapterTestCase, self).setUp()
        import requests

        requests.post = Mock(side_effect=mock_post_response)

        gitter.requests = requests

        self.adapter = Gitter(
            gitter_room='',
            gitter_api_token='',
            gitter_sleep_time=0,
            gitter_only_respond_to_mentions=False
        )

    def test_validate_status_code_200(self):
        response = MockResponse(200, {})

        try:
            self.adapter._validate_status_code(response)
        except Gitter.HTTPStatusException:
            self.fail('Test raised HTTPStatusException unexpectedly!')

    def test_validate_status_code_201(self):
        response = MockResponse(201, {})

        try:
            self.adapter._validate_status_code(response)
        except Gitter.HTTPStatusException:
            self.fail('Test raised HTTPStatusException unexpectedly!')

    def test_response_status_code_not_ok(self):
        response = MockResponse(404, {})

        with self.assertRaises(Gitter.HTTPStatusException):
            self.adapter._validate_status_code(response)

    def test_join_room(self):
        data = self.adapter.join_room('room_name')
        self.assertIn('id', data)

    def test_send_message(self):
        pass

    def test_process_response(self):
        statement = Statement('Hello')
        output_statement = self.adapter.process_response(statement)

        self.assertEqual(output_statement, statement)
