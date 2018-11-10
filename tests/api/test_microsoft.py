from unittest.mock import Mock
from tests.base_case import ChatBotTestCase
from chatterbot.api import microsoft


class MockResponse(object):

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


def mock_post_request(*args, **kwargs):
    url = args[0]
    endpoints = {
        'https://directline.botframework.com/api/conversations': MockResponse(
            200,
            {
                "conversationId": "IEyJvnDULgn",
                "token": (
                    "xtFDtPemROU.dAA.MgBPAGUAUQBnADEAWgB2AGUAYwA3AA.oWyal9M70g"
                    "E.XJEMr9FNGGI.6UCCu0-lLSLplLZ0MVDk_rMle7DItjF-KFSIUTUjUR8"
                ),
                "expires_in": 0
            }
        ),
        'https://directline.botframework.com/api/conversations/IEyJvnDULgn/messages': MockResponse(
            204, 'no content'
        )

    }

    return endpoints[url]


def mock_get_request(*args, **kwargs):
    url = args[0]
    endpoints = {
        'https://directline.botframework.com/api/conversations/IEyJvnDULgn/messages': MockResponse(200, {
            "messages": [
                {
                    "id": "IEyJvnDULgn|000000000000000001",
                    "conversationId": "IEyJvnDULgn",
                    "created": "2016-11-04T15:26:57.9186086Z",
                    "from": "malli.kv2@gmail.com",
                    "images": [],
                    "attachments": [
                        {
                            "url": (
                                "/attachments/IEyJvnDULgn/000000000000000001/0/testregexp.txt"
                                "?t=xtFDtPemROU.dAA.SQBFAHkASgB2AG4ARABVAEwAZwBuAC0AMAAwADAAM"
                                "AAwADAAMAAwADAAMAAwADAAMAAwADAAMAAwADEA.67FrGrs20gE.-Hqfw5g3"
                                "NgM.eJZ8WI_v78i1OBZ0zF4jLjuOpKrw2WF0PmqSgEhWIYw"
                            ),
                            "contentType": "text/plain"
                        }
                    ],
                    "eTag": "W/\"datetime'2016-11-04T15%3A26%3A58.3595526Z'\""
                },
                {
                    "id": "IEyJvnDULgn|000000000000000002",
                    "conversationId": "IEyJvnDULgn",
                    "created": "2016-11-04T15:27:00.2245784Z",
                    "from": "bc-directlinedocs-testbot",
                    "text": "Hi! What is your name?",
                    "images": [],
                    "attachments": [],
                    "eTag": "W/\"datetime'2016-11-04T15%3A27%3A00.663327Z'\""
                }
            ],
            "watermark": "2"
        })
    }

    return endpoints[url]


class MicrosoftTestCase(ChatBotTestCase):

    def setUp(self):
        super().setUp()
        import requests

        requests.post = Mock(side_effect=mock_post_request)
        requests.get = Mock(side_effect=mock_get_request)

        microsoft.requests = requests


class MicrosoftTests(MicrosoftTestCase):

    def test_validate_status_code_200(self):
        response = MockResponse(200, {})

        try:
            microsoft._validate_status_code(response)
        except microsoft.HTTPStatusException:
            self.fail('Test raised HTTPStatusException unexpectedly!')

    def test_response_status_code_not_ok(self):
        response = MockResponse(404, {})
        with self.assertRaises(microsoft.HTTPStatusException):
            microsoft._validate_status_code(response)

    def test_start_conversation(self):
        data = microsoft.start_conversation('fake_access_token')
        self.assertIn('conversationId', data)
        self.assertIn('token', data)
        self.assertIn('expires_in', data)
