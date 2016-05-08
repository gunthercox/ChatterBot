from chatterbot.adapters.input import InputAdapter
from chatterbot.utils.read_input import input_function


JSON = 'json'
TEXT = 'text'
OBJECT = 'object'
VALID_FORMATS = (JSON, TEXT, OBJECT, )


class InputFormatAdapter(InputAdapter):
    """
    The NoOutputAdapter is a simple adapter that
    doesn't display anything.
    """

    def __init__(self, *args, **kwargs):
        super(InputFormatAdapter, self).__init__(**kwargs)
        self.format = kwargs.get('format', 'object')

        if self.format not in VALID_FORMATS:
            pass

        if self.format == TEXT:
            pass

        if self.format == JSON:
            # Convert input json data into a statement object
            if not args and self.format == JSON:
                # TODO subclass this error
                raise TypeError(
                    "process_input expects at least one positional argument"
                )

            input_json = args[0]
            text = input_json["text"]
            del(input_json["text"])

            return Statement(text, **input_json)

        # TODO: Should this just be a parameter for the Terminal adapter?
        # Read the user's input from the terminal.
        user_input = input_function()
        return Statement(user_input)

    def process_input(self, *args, **kwargs):
        pass
