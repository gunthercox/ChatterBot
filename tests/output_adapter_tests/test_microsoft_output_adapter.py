from unittest import TestCase
from unittest.mock import Mock
from chatterbot.conversation import Statement
from chatterbot.output import Microsoft
from chatterbot.output import microsoft


class MockResponse(object):

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


def mock_start_conversation(*args, **kwargs):
    url = args[0]
    endpoints = {
        'https://directline.botframework.com/api/conversations': MockResponse(
            200,
            {
                "conversationId": "IEyJvnDULgn",
                "token": (
                    "xtFDtPemROU.dAA.MgBPAGUAUQBnADEAWgB2AGUAYwA3AA.oWyal9M70"
                    "gE.XJEMr9FNGGI.6UCCu0-lLSLplLZ0MVDk_rMle7DItjF-KFSIUTUjUR8"
                ),
                "expires_in": 0
            }
        )
    }

    return endpoints[url]


def mock_send_message(*args, **kwargs):
    url = args[0]
    directline_url = 'https://directline.botframework.com/api/conversations/IEyJvnDULgn/messages'
    endpoints = {
        directline_url: MockResponse(204, 'no content')
    }

    return endpoints[url]


def mock_get_message(*args, **kwargs):
    url = args[0]
    directline_url = 'https://directline.botframework.com/api/conversations/IEyJvnDULgn/messages'
    endpoints = {
        directline_url: MockResponse(200, {
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
                                "/attachments/IEyJvnDULgn/000000000000000001/0/"
                                "testregexp.txt?t=xtFDtPemROU.dAA.SQBFAHkASgB2A"
                                "G4ARABVAEwAZwBuAC0AMAAwADAAMAAwADAAMAAwADAAMAA"
                                "wADAAMAAwADAAMAAwADEA.67FrGrs20gE.-Hqfw5g3NgM."
                                "eJZ8WI_v78i1OBZ0zF4jLjuOpKrw2WF0PmqSgEhWIYw"
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


class MicrosoftAdapterTests(TestCase):

    def setUp(self):
        super(MicrosoftAdapterTests, self).setUp()
        import requests

        requests.post = Mock(side_effect=mock_send_message)
        requests.get = Mock(side_effect=mock_get_message)

        microsoft.requests = requests

        self.adapter = Microsoft(
            directline_host='https://directline.botframework.com',
            direct_line_token_or_secret='xtFDtPemROU.cwA.Mcs.qiScdaSx87ffj2l7OjSITqJFoN-9Ado5AgwVeknac94',
            conversation_id='IEyJvnDULgn'
        )

    def test_validate_status_code_200(self):
        response = MockResponse(200, {})

        try:
            self.adapter._validate_status_code(response)
        except Microsoft.HTTPStatusException:
            self.fail('Test raised HTTPStatusException unexpectedly!')

    def test_response_status_code_not_ok(self):
        response = MockResponse(404, {})
        with self.assertRaises(Microsoft.HTTPStatusException):
            self.adapter._validate_status_code(response)

    def test_process_response(self):
        statement = Statement('Hi! What is your name?')
        data = self.adapter.process_response(statement)
        self.assertEqual('Hi! What is your name?', data)
