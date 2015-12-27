from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def __init__(self, **kwargs):
        super(LogicAdapter, self).__init__(**kwargs)

        self.tie_breaking_method = kwargs.get(
            "tie_breaking_method",
            "first_response"
        )

    def process(self, statement):
        """
        Method that takes an input statement and returns
        a statement as output.
        """
        raise AdapterNotImplementedError()

