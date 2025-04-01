from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class Ollama(LogicAdapter):
    """
    This adapter allows the use of Ollama models for chatbot responses.

    .. warning::
        This is a new and experimental adapter. It may not work as expected
        and its functionality may change in future releases.

    .. note::
        Added in version 1.2.5
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from ollama import Client, AsyncClient

        self.model = kwargs.get('model', 'gemma3:1b')  # TODO: Better default model?
        self.host = kwargs.get('host', 'http://localhost:11434')

        # TODO: Look into supporting the async client
        self.async_mode = False

        # https://github.com/ollama/ollama-python
        if self.async_mode:
            self.client = AsyncClient(
                host=self.host,
            )
        else:
            self.client = Client(
                host=self.host,
            )

    def process(self, statement, additional_response_selection_parameters=None):

        system_message = {
            'role': 'system',
            'content': 'Please keep responses short and concise.'
        }
        message = {
            'role': 'user',
            'content': statement.text
        }

        if self.chatbot.stream:
            for part in self.client.chat(
                model=self.model,
                messages=[system_message, message],
                stream=True
            ):
                yield part['message']['content']
        else:
            response = self.client.chat(
                model=self.model,
                messages=[system_message, message]
            )

            response = Statement(text=response.message.content)

            # Confidence will be a 1 for all responses
            # TODO: Is there a better way to score confidence for LLM based responses?
            response.confidence = 1

            return response
