import asyncio

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

        # The async client can only be used when the ChatBot has
        # been initialized with 1 logic adapter.
        '''
        if len(self.chatbot.logic_adapters) == 1:
            self.async_mode = True
            self.client = client = AsyncClient(
                host=self.host,
            )
        else:
        '''
        self.async_mode = False
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

        # TODO Add support for streaming responses
        '''
        if self.async_mode:
            async def chat():
                async for part in await self.client.chat(
                    model=self.model,
                    messages=[system_message, message],
                    stream=True
                ):
                    print(part['message']['content'], end='', flush=True)

                print()

                asyncio.run(chat())'
        '''

        # https://github.com/ollama/ollama-python
        response = self.client.chat(model=self.model, messages=[
            system_message,
            message
        ])

        response = Statement(text=response.message.content)

        response.confidence = 1  # TODO: Better way to determine confidence?

        return response
