from datetime import datetime
from chatterbot import languages
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.utils import get_model_for_language
from chatterbot.logic.mcp_tools import MCPToolAdapter
import spacy


class TimeLogicAdapter(LogicAdapter, MCPToolAdapter):
    """
    The TimeLogicAdapter returns the current time.

    :kwargs:
        * *positive* (``list``) --
          The time-related questions used to identify time questions about the current time.
          Defaults to a list of English sentences.
        * *language* (``str``) --
          The language for the spacy model. Defaults to English.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        # TODO / FUTURE: Switch `positive` to `patterns` for more accurate naming
        phrases = kwargs.get('positive', [
            'What time is it?',
            'Hey, what time is it?',
            'Do you have the time?',
            'Do you know the time?',
            'Do you know what time it is?',
            'What is the time?',
            'What time is it now?',
            'Can you tell me the time?',
            'Could you tell me the time?',
            'What is the current time?',
        ])

        language = kwargs.get('language', languages.ENG)

        model = get_model_for_language(language)

        self.nlp = spacy.load(model)

        # Set up rules for spacy's rule-based matching
        # https://spacy.io/usage/rule-based-matching

        self.matcher = spacy.matcher.PhraseMatcher(self.nlp.vocab)

        patterns = [self.nlp.make_doc(text) for text in phrases]

        # Add the patterns to the matcher
        self.matcher.add('TimeQuestionList', patterns)

    def process(self, statement: Statement, additional_response_selection_parameters: dict = None) -> Statement:
        now = datetime.now()

        # Check if the input statement contains a time-related question
        doc = self.nlp(statement.text)

        matches = self.matcher(doc)

        self.chatbot.logger.info('TimeLogicAdapter detected {} matches'.format(len(matches)))

        confidence = 1 if matches else 0
        response = Statement(text='The current time is ' + now.strftime('%I:%M %p'))

        response.confidence = confidence
        return response

    def get_tool_schema(self):
        """
        Return the MCP tool schema for getting current time.
        """
        return {
            "name": "get_current_time",
            "description": "Get the current date and time. Returns formatted time string.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

    def execute_as_tool(self, **kwargs):
        """
        Execute time query as a tool.

        Returns:
            Current time as formatted string
        """
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"
