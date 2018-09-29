from chatterbot.output import OutputAdapter
from chatterbot.api import microsoft


class Microsoft(OutputAdapter):
    """
    An output adapter that allows a ChatterBot instance to send
    responses to a Microsoft bot using *Direct Line client protocol*.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.direct_line_token_or_secret = kwargs.get(
            'direct_line_token_or_secret'
        )
        self.conversation_id = kwargs.get('conversation_id')

    def process_response(self, statement):
        data = microsoft.send_message(
            self.direct_line_token_or_secret,
            self.conversation_id,
            statement.text
        )
        self.chatbot.logger.info('processing user response {}'.format(data))
        return statement
