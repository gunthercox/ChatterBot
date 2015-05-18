from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(object):

    def get_response(self):
        raise AdapterNotImplementedError()
