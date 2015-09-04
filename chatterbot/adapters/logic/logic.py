from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(object):

    def get(self):
        raise AdapterNotImplementedError()
