from time import sleep
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement
from chatterbot.api import microsoft


class Microsoft(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a Microsoft Bot using *Directline client protocol*.
    https://docs.botframework.com/en-us/restapi/directline/#navtitle
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # NOTE: Direct Line client credentials are different from your bot's credentials
        self.direct_line_token_or_secret = kwargs.get(
            'direct_line_token_or_secret'
        )

        conversation_data = microsoft.start_conversation(self.direct_line_token_or_secret)
        self.conversation_id = conversation_data.get('conversationId')
        self.conversation_token = conversation_data.get('token')

    def process_input(self, statement):
        new_message = False
        data = None
        while not new_message:
            data = microsoft.get_most_recent_message(
                self.direct_line_token_or_secret,
                self.conversation_id
            )
            if data and data['id']:
                new_message = True
            else:
                pass
            sleep(3.5)

        text = data['text']
        statement = Statement(text)
        self.logger.info('processing user statement {}'.format(statement))

        return statement
