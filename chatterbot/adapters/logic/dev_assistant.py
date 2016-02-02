from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement

from chatterbot.utils.stop_words import StopWordsManager
from chatterbot.utils.pos_tagger import POSTagger

import subprocess


class DeveloperAssistant(LogicAdapter):
    """
    The DeveloperAssistant logic adapter provides a set of tools
    that can help a developer program. Currently, only the following
    features are supported:
    1) Running Python programs
    """

    def __init__(self, **kwargs):
        super(DeveloperAssistant, self).__init__(**kwargs)

        # Initializing variables
        self.program_path = ""
        self.program_name = ""
        self.stage = 0

        self.stopwords = StopWordsManager()
        self.tagger = POSTagger()
        self.conversation = []

    def process(self, statement):
        """
        Assuming the user inputed statement is a
        request for the developer assistant, parse
        the request and determine the appropriate
        action to be used.
        """
        confidence = 0

        # Getting the conversation
        try:
            self.conversation = self.context.conversation
        except:
            pass

        # Getting the stage of interaction with the user (assuming a command has not been executed)
        if self.stage != 3:
            confidence = self.determine_stage_of_interaction(statement)

        if self.stage == 1:
            return confidence, Statement("What is the absolute path to " + self.program_name + "?")
        elif self.stage == 3:
            # Run program
            self.context.io.process_response(Statement("Running " + self.program_name + "..."))
            subprocess.Popen("python " + self.program_path + self.program_name, shell=True)

            # Resetting global variables
            self.program_name = ""
            self.program_path = ""
            self.stage = 0

            # Return a response
            return confidence, Statement("The program has finished running")

        return 0, Statement("")

    def determine_stage_of_interaction(self, input_statement):
        """
        Determines at which point in the interaction with
        the user chatterbot is.
        """
        confidence = 0

        length = len(self.conversation)
        if length == 0:
            length = 1

        # Parsing through the conversation with chatterbot looking for information
        # @TODO: Find a way to store run programs --> Currently there is an
        #   issue where if the user tries to run multiple programs in a single
        #   ChatterBot instance, it will not always pick the correct program.
        #   To fix this, the previous programs run need to be saved & only the
        #   most recent program in the conversation log needs to be saved.
        user_input = ""
        for conversation_index in range(0, length):
            if conversation_index == 0:
                user_input = input_statement.text
            else:
                user_input = self.conversation[length - conversation_index][0]

            if self.program_name is "":
                extracted_name = self.extract_name(user_input)
                if extracted_name is not "":
                    self.program_name = extracted_name
                    self.stage += 1

            if self.program_path is "":
                extracted_path = self.extract_path(user_input)
                if extracted_path is not "":
                    self.program_path = extracted_path
                    self.stage += 2

        if self.stage != 0:
            confidence = 1

        return confidence

    def extract_name(self, user_input):
        """
        Return the program's name if it is included somewhere in the
        conversation.
        """
        name = ""

        # The following assumes that the user_input is simply: "run program_x"
        # @TODO: Change this to a more advanced parsing of the user_input. It
        #   requires additional functions within the chatterbot.utils module
        #   and some more thought on how to implement a better system
        has_asked_run = False
        for token in self.tagger.tokenize(user_input):
            if has_asked_run:
                if "/" in token:
                    name = token.split("/")[len(token.split("/")) - 1]
                else:
                    name = token
                break

            if "run" in token:
                has_asked_run = True

        return name

    def extract_path(self, user_input):
        """
        Return the program's path if it is included somewhere in the
        conversation.
        """
        path = ""

        # Identifies the path if one is in user_input
        # @TODO: Rewrite to remove false positives (which can be created
        #   easily with the current implementation)
        for word in self.tagger.tokenize(user_input):
            if "/" in word:
                if word.endswith("/"):
                    path = word
                else:
                    split = word.split("/")
                    path = "/".join(split[:len(split) - 1]) + "/"
                break

        return path
