from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
from chatterbot.utils.trees import find_sequence_in_tree


class SubtreeMatchingTestCase(ChatBotTestCase):

    def test_exact_match(self):
        sequence = [
            Statement('Hi, how are you?'),
            Statement('I am good, how about you?'),
            Statement('I am also good.')
        ]

        self.chatbot.set_trainer(ListTrainer)
        self.chatbot.train([
            sequence[0].text, sequence[1].text, sequence[2].text
        ])

        found = find_sequence_in_tree(self.chatbot.storage, sequence)

        self.assertEqual(len(found), len(sequence))

    def test_no_match(self):
        pass

    def test_close_match(self):
        pass

    def test_partial_sequence_match(self):
        pass

    def test_partial_tree_match(self):
        pass
