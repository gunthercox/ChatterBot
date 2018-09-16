from .output_adapter import OutputAdapter


class TerminalAdapter(OutputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_response(self, statement):
        """
        Print the response to the user's input.
        """
        print(statement.text)
        return statement.text
