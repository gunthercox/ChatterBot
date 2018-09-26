from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement
from chatterbot.api import mailgun


class Mailgun(InputAdapter):
    """
    Get input from Mailgun.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Use the bot's name for the name of the sender
        self.name = kwargs.get('name')
        self.from_address = kwargs.get('mailgun_from_address')
        self.api_key = kwargs.get('mailgun_api_key')
        self.endpoint = kwargs.get('mailgun_api_endpoint')

    def process_input(self, statement):
        urls = mailgun.get_stored_email_urls(self.api_key, self.endpoint)
        url = list(urls)[0]

        response = mailgun.get_message(self.api_key, url)
        message = response.json()

        text = message.get('stripped-text')

        return Statement(text)
