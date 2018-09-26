from chatterbot.output import OutputAdapter
from chatterbot.api import mailgun


class Mailgun(OutputAdapter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Use the bot's name for the name of the sender
        self.name = kwargs.get('name')
        self.from_address = kwargs.get('mailgun_from_address')
        self.api_key = kwargs.get('mailgun_api_key')
        self.endpoint = kwargs.get('mailgun_api_endpoint')
        self.recipients = kwargs.get('mailgun_recipients')

    def process_response(self, statement):
        """
        Send the response statement as an email.
        """
        subject = 'Message from %s' % (self.name)

        mailgun.send_message(
            self.api_key,
            self.endpoint,
            self.name,
            subject,
            statement.text,
            self.from_address,
            self.recipients
        )

        return statement
