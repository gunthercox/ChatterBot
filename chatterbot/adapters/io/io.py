from chatterbot.adapters.exceptions import AdapterNotImplementedError


class IOAdapter(object):

    def get_response(self, input_value):
        """
        Takes an input value.
        Returns an output value.
        """
        raise AdapterNotImplementedError()
