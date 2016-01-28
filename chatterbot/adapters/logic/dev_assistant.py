from chatterbot.adapters.exceptions import EmptyDatasetException
from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement

from chatterbot.utils.stop_words import StopWordsManager
from chatterbot.utils.pos_tagger import POSTagger

from textblob.classifiers import NaiveBayesClassifier

import subprocess


class DeveloperAssistant(LogicAdapter):

    def __init__(self, **kwargs):
        super(DeveloperAssistant, self).__init__(**kwargs)

        # Initializing all variables
        self.program_path = ""
        self.program_name = ""

        # Training the classifier
        training_data = [
            ("run the program located at", 1),
            ("run", 1),
            ("run ", 1),
            ("run program", 1),
            ("what is the output of the program", 1),
            ("what time is it", 0),
            ("what is", 0),
            ("hello", 0),
            ("time", 0),
            ("where are you", 0),
            ("who is this", 0)
        ]

        self.classifier = NaiveBayesClassifier(training_data)

        self.stopwords = StopWordsManager()
        self.tagger = POSTagger()

    def process(self, statement):
        """
        Assuming the user inputed statement is a
        request for the developer assistant, parse
        the request and determine the appropriate
        action to be used.
        """
        # Getting the confidence of this adapter's ability to respond
        # @TODO: This should not be as simple as a NaiveBayesClassifier
        #   but should instead use some way to determine how likely it
        #   is that the user is interacting with this logic adapter.
        confidence = self.classifier.classify(statement.text)

        # Getting the stage of interaction with the user
        stage = self.determine_stage_of_interaction(statement)

        if stage == 0 or stage == 2:
            return confidence, Statement("What is the name of the program?")
        elif stage == 1:
            return confidence, Statement("What is the absolute path to " + self.program_name + "?")
        elif stage == 3:
            # Run program
            self.context.io.process_response(Statement("Running " + self.program_name + "..."))
            subprocess.call(['python', self.program_path, self.program_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Resetting global variables
            self.program_name = ""
            self.program_path = ""

            # Return a response
            return confidence, Statement("The program has finished running")

        return 0, Statement("")

    def determine_stage_of_interaction(self, input_statement):
        """
        Determines at which point in the interaction with
        the user chatterbot is.
        """
        user_has_given_name = False
        user_has_given_path = False
        stage = 0

        # Parsing through the conversation with chatterbot looking for information
        for conversation_index in xrange(len(self.context.conversation), 0, -1):
            if conversation_index < len(self.context.conversation):
                conversation = self.context.conversation[conversation_index]
                user_input = conversation[0]
            else:
                user_input = input_statement.text

            if self.extract_name(user_input) is not "" and user_has_given_name == False:
                user_has_given_name = True
                stage = 1
                self.program_name = self.extract_name(user_input)

            if self.extract_path(user_input) is not "" and user_has_given_path == False:
                user_has_given_path = True
                stage += 2
                self.program_path = self.extract_path(user_input)

        return stage

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
        if len(self.tagger.tokenize(user_input)) > 1:
            name = self.tagger.tokenize(user_input)[1]

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
        for word in user_input.split():
            if "/" in word:
                path = word
                break

        return path
