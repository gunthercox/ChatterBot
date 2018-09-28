from unittest.mock import Mock
from tests.base_case import ChatBotTestCase
from chatterbot.api import gitter


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
        'https://api.gitter.im/v1/rooms/40999743/chatMessages': MockResponse(200, data),
        'https://api.gitter.im/v1/user/9893893/rooms/40999743/unreadItems': MockResponse(200, {'id': '343222'})
    }

    return endpoints[url]


class GitterTestCase(ChatBotTestCase):

    def setUp(self):
        super().setUp()
        import requests

        requests.get = Mock(side_effect=mock_get_response)
        requests.post = Mock(side_effect=mock_post_response)

        gitter.requests = requests


class GitterTests(GitterTestCase):

    def test_validate_status_code_200(self):
        response = MockResponse(200, {})

        try:
            gitter._validate_status_code(response)
        except gitter.HTTPStatusException:
            self.fail('Test raised HTTPStatusException unexpectedly!')

    def test_validate_response_201(self):
        response = MockResponse(201, {})

        try:
            gitter._validate_status_code(response)
        except gitter.HTTPStatusException:
            self.fail('Test raised HTTPStatusException unexpectedly!')

    def test_response_status_code_not_ok(self):
        response = MockResponse(404, {})
        with self.assertRaises(gitter.HTTPStatusException):
            gitter._validate_status_code(response)

    def test_join_room(self):
        data = gitter.join_room('fake_access_token', 'room_name')
        self.assertIn('id', data)

    def test_send_message(self):
        raise self.skipTest('This test needs to be created.')

    def test_get_user_data(self):
        data = gitter.get_user_data('fake_access_token')
        self.assertIn('id', data[0])

    def test_mark_messages_as_read(self):
        room_id = '40999743'
        user_id = '9893893'
        data = gitter.mark_messages_as_read('fake_access_token', user_id, room_id, [1, 2, 3])
        self.assertIn('id', data)

    def test_get_most_recent_message(self):
        room_id = '40999743'
        data = gitter.get_most_recent_message('fake_access_token', room_id)
        self.assertIn('text', data)
        self.assertIn('id', data)
        self.assertIn('unread', data)

    def test_contains_mention(self):
        contains = gitter._contains_mention([{'screenName': 'chatterbot'}], 'chatterbot')
        self.assertTrue(contains)

    def test_does_not_contain_mention(self):
        contains = gitter._contains_mention([{'screenName': 'coolguy'}], 'chatterbot')
        self.assertFalse(contains)

    def test_should_respond_no_data(self):
        should = gitter.should_respond({}, 'username', False)
        self.assertFalse(should)

    def test_should_respond_unread(self):
        should = gitter.should_respond({'unread': True}, 'username', False)
        self.assertTrue(should)

    def test_remove_mentions(self):
        cleaned = gitter.remove_mentions('Hi @person how are you @myfriend')
        self.assertEqual(cleaned, 'Hi how are you')
