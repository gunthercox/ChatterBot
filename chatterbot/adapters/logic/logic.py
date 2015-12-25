from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def get(self, text, statement_list=None):
        raise AdapterNotImplementedError()

    def get_statements_with_known_responses(self):
        """
        Filter out all statements that are not in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        """
        if (not self.context) or (not self.context.storage):
            return []

        all_statements = self.context.storage.filter()

        responses = set()
        to_remove = list()
        for statement in all_statements:
            for response in statement.in_response_to:
                responses.add(response.text)
        for statement in all_statements:
            if statement.text not in responses:
                to_remove.append(statement)

        for statement in to_remove:
            all_statements.remove(statement)

        return all_statements

