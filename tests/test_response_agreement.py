from unittest import TestCase

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.tagging import NoOpTagger


class FixedResponseAdapter(LogicAdapter):

    def __init__(self, chatbot, response):
        super().__init__(chatbot)
        self.response = response

    def process(self, statement, additional_response_selection_parameters=None):
        return self.response


class ResponseAgreementTests(TestCase):

    def setUp(self):
        self.chatbot = ChatBot(
            'Voting Bot',
            database_uri=None,
            initialize=False,
            read_only=True,
            tagger=NoOpTagger,
            logic_adapters=[],
        )
        self.addCleanup(self.chatbot.storage.close)
        self.addCleanup(self.chatbot.storage.drop)

    def get_response(self, options):
        self.chatbot.logic_adapters = [
            FixedResponseAdapter(self.chatbot, option) for option in options
        ]
        return self.chatbot.get_response('What is the answer?')

    def test_colons_do_not_create_false_agreement(self):
        cases = (
            (('Status: ready', 'Report'), ('Status', ' ready:Report')),
            (('Status:', None), ('Status', ':')),
            ((':Status', 'Report'), ('', 'Status:Report')),
        )
        for first, second in cases:
            with self.subTest(first=first, second=second):
                response = self.get_response([
                    Statement('Preferred answer', confidence=1),
                    Statement(first[0], in_response_to=first[1], confidence=0.2),
                    Statement(second[0], in_response_to=second[1], confidence=0.3),
                ])
                self.assertEqual(response.text, 'Preferred answer')
                self.assertEqual(response.confidence, 1)

    def test_matching_pairs_with_colons_still_agree(self):
        response = self.get_response([
            Statement('Alternative', confidence=1),
            Statement('Status: ready', in_response_to='Report: now', confidence=0.2),
            Statement('Status: ready', in_response_to='Report: now', confidence=0.6),
        ])
        self.assertEqual(response.text, 'Status: ready')
        self.assertEqual(response.confidence, 0.6)

    def test_missing_and_empty_previous_text_still_agree(self):
        response = self.get_response([
            Statement('Alternative', confidence=1),
            Statement('Status: ready', in_response_to=None, confidence=0.2),
            Statement('Status: ready', in_response_to='', confidence=0.6),
        ])
        self.assertEqual(response.text, 'Status: ready')
        self.assertEqual(response.confidence, 0.6)
