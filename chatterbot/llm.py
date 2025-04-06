"""
Large Language Model (LLM) clients.

    .. note::
        As a part of the development process when choosing models it is
        important to research and understand the models you are using.

        A good example of why this is important can be found in the
        description of the Phi-3 model from Microsoft which discusses
        responsible AI considerations such as the limitations of the
        model, and appropriate use cases.
        https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf#responsible-ai-considerations
"""


class ModelClient:
    """
    A base class to define the interface for language model clients.
    """

    def __init__(self, chatbot, model: str, **kwargs):
        self.chatbot = chatbot
        self.model = model


class Ollama(ModelClient):
    """
    This client class allows the use of Ollama models for chatbot responses.

    .. warning::
        This is a new and experimental class. It may not work as expected
        and its functionality may change in future releases.

    .. note::
        Added in version 1.2.7
    """

    def __init__(self, chatbot, model: str, **kwargs):
        """
        keyword arguments:
            host: The host URL for the Ollama server.
                Default is 'http://localhost:11434'.
        """
        super().__init__(chatbot, model)
        from ollama import Client, AsyncClient

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

    def process(self, statement):

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

            return response.message.content


class OpenAI(ModelClient):
    """
    This client class allows the use of the OpenAI API to generate chatbot responses.

    .. warning::
        This is a new and experimental class. It may not work as expected
        and its functionality may change in future releases.

    .. note::
        Added in version 1.2.7
    """

    def __init__(self, chatbot, model, **kwargs):
        super().__init__(chatbot, model, **kwargs)
        from openai import OpenAI as OpenAIClient
        from openai import AsyncOpenAI as AsyncOpenAIClient

        self.host = kwargs.get('host', None)

        # TODO: Look into supporting the async client
        self.async_mode = False

        # https://github.com/openai/openai-python
        if self.async_mode:
            self.client = AsyncOpenAIClient(
                base_url=self.host,
            )
        else:
            self.client = OpenAIClient(
                base_url=self.host,
            )

    def process(self, statement):

        system_message = {
            'role': 'developer',
            'content': 'Please keep responses short and concise.'
        }
        message = {
            'role': 'user',
            'content': statement.text
        }

        if self.chatbot.stream:
            for part in self.client.chat.completions.create(
                model=self.model,
                messages=[system_message, message],
                stream=True
            ):
                yield part
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[system_message, message]
            )

            return response.output_text
