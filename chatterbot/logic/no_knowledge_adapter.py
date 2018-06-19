from .logic_adapter import LogicAdapter


class NoKnowledgeAdapter(LogicAdapter):
    """
    This is a system adapter that is automatically added
    to the list of logic adapters during initialization.
    This adapter is placed at the beginning of the list
    to be given the highest priority.
    """

    def process(self, statement):
        """
        If there are no known responses in the database,
        then a confidence of 1 should be returned with
        the input statement.
        Otherwise, a confidence of 0 should be returned.
        """

        if self.chatbot.storage.count():
            statement.confidence = 0
        else:
            statement.confidence = 1

        return statement
