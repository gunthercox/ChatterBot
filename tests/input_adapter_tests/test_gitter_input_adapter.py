from unittest import TestCase
from mock import Mock
from chatterbot.conversation import Statement
from chatterbot.input import gitter
from chatterbot.input import Gitter


class MockResponse(object):

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


def mock_get_response(*args, **kwargs):
    url = args[0]

    endpoints = {
        'https://api.gitter.im/v1/user': MockResponse(200, [{'id': '9893893'}]),
        'https://api.gitter.im/v1/rooms/40999743/chatMessages?limit=1': MockResponse(200, [
            {'id': '4467', 'text': 'Hello', 'unread': True}
        ])
    }

    return endpoints[url]


def mock_post_response(*args, **kwargs):
    url = args[0]
    data = kwargs.get('data', {})

    endpoints = {
        'https://api.gitter.im/v1/rooms': MockResponse(200, {'id': '40999743'}),
        'https://api.gitter.im/v1/user/9893893/rooms/40999743/unreadItems': MockResponse(200, {'id': '343222'})
    }

    return endpoints[url]


class GitterAdapterTests(TestCase):

    def setUp(self):
        super(GitterAdapterTests, self).setUp()
        import requests

        requests.get = Mock(side_effect=mock_get_response)
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

    def test_validate_response_201(self):
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

    def test_get_user_data(self):
        data = self.adapter.get_user_data()
        self.assertIn('id', data[0])

    def test_mark_messages_as_read(self):
        data = self.adapter.mark_messages_as_read([1, 2, 3])
        self.assertIn('id', data)

    def test_get_most_recent_message(self):
        data = self.adapter.get_most_recent_message()
        self.assertIn('text', data)
        self.assertIn('id', data)
        self.assertIn('unread', data)

    def test_contains_mention(self):
        self.adapter.username = 'chatterbot'
        contains = self.adapter._contains_mention([{'screenName': 'chatterbot'}])
        self.assertTrue(contains)

    def test_does_not_contain_mention(self):
        self.adapter.username = 'chatterbot'
        contains = self.adapter._contains_mention([{'screenName': 'coolguy'}])
        self.assertFalse(contains)

    def test_should_respond_no_data(self):
        should = self.adapter.should_respond({})
        self.assertFalse(should)

    def test_should_respond_unread(self):
        should = self.adapter.should_respond({'unread': True})
        self.assertTrue(should)

    def test_remove_mentions(self):
        cleaned = self.adapter.remove_mentions('Hi @person how are you @myfriend')
        self.assertEqual(cleaned, 'Hi how are you')

    def test_process_input(self):
        statement = Statement('Hello')
        data = self.adapter.process_input(statement)
        self.assertEqual('Hello', data)
