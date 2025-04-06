from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class OpenAI(LogicAdapter):
    """
    This adapter allows the use of the OpenAI API to generate chatbot responses.

    .. warning::
        This is a new and experimental adapter. It may not work as expected
        and its functionality may change in future releases.

    .. note::
        Added in version 1.2.7

    .. note::
        As a part of the development process when choosing models it is
        important to research and understand the models you are using.

        A good example of why this is important can be found in the
        description of the Phi-3 model from Microsoft which discusses
        responsible AI considerations such as the limitations of the
        model, and appropriate use cases.
        https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf#responsible-ai-considerations
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from openai import OpenAI as OpenAIClient
        from openai import AsyncOpenAI as AsyncOpenAIClient

        self.model = kwargs.get('model', 'gpt-4o')
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

    def process(self, statement, additional_response_selection_parameters=None):

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

            response = Statement(text=response.output_text)

            # Confidence will be a 1 for all responses
            # TODO: Is there a better way to score confidence for LLM based responses?
            response.confidence = 1

            return response
