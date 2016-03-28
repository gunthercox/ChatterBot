from chatterbot.adapters.io import IOAdapter
from chatterbot.conversation import Statement


class JsonAdapter(IOAdapter):
    """
    The JsonAdapter class returns a python dictionary which
    is useful for serialization and deserialization of statements.
    """

    def process_input(self, *args, **kwargs):
        """
        Convert input json data into a statement object.
        """
        if not args:
            raise TypeError(
                "process_input expects at least one positional argument"
            )

        input_json = args[0]
        text = input_json["text"]
        del(input_json["text"])

        return Statement(text, **input_json)

    def process_response(self, statement):
        return statement.serialize()
