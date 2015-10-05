from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(object):

    def get(self, text, list_of_statements, current_conversation=None):
        raise AdapterNotImplementedError()
