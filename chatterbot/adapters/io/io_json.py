from chatterbot.adapters.io import IOAdapter
from chatterbot.conversation import Statement


class JsonAdapter(IOAdapter):

    def process_input(self, input_json):
        """
        Convert input json data into a statement object.
        """
        text = input_json["text"]
        del(input_json["text"])

        return Statement(text, **input_json)

    def process_response(self, statement):
        return statement.serialize()
