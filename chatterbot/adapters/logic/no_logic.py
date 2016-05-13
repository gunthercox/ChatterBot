from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement


class NoLogic(LogicAdapter):

    def can_process(self, statement):
        """
        Determines if this adapter can respond to the input.
        """
        return True

    def process(self, statement):
        import random

        # Get all statements that are in response to the closest match
        response_list = self.context.storage.filter(
            in_response_to__contains=statement.text
        )

        return 1, random.choice(response_list)
