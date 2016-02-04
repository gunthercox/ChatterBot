from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement

from chatterbot.utils.stop_words import StopWordsManager
from chatterbot.utils.pos_tagger import POSTagger

import subprocess
import os
import json


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
        self.program_data = { "name" : "", "path" : "" }
        self.stage = ""
        self.data_dir = ""
        self.data = self.read_program_file()

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
        if self.stage is not "name path":
            self.data = self.read_program_file()
            confidence = self.determine_stage_of_interaction(statement)

        if self.stage is "name":
            return confidence, Statement("What is the absolute path to " + self.program_data["name"] + "?")
        elif "previously_used" in self.stage:
            return confidence, Statement("Would you like to use the path " + self.program_data["suggested_path"] + "?")
        elif "name path" in self.stage:
            # Run program
            subprocess.Popen("python " + self.program_data["path"] + self.program_data["name"], shell=True)
            return_statement = Statement("Running " + self.program_data["name"] + "...")
            self.update_data()

            # Resetting global variables
            self.program_data = { "name" : "", "path" : "" }
            self.stage = ""

            # Return a response
            return confidence, return_statement

        return 0, Statement("")

    def read_program_file(self):
        """
        Read in the programs that have been run previously.
        """
        path = self.data_dir + "programs_run.json"
        if os.path.exists(path):
            with open(path, 'r') as data_file:
                try:
                    return json.load(data_file)
                except:
                    pass

        empty_data = {
            "programs_run": {
            }
        }

        return empty_data

    def write_program_file(self):
        """
        Write the programs that have been previously run.
        """
        path = self.data_dir + "programs_run.json"
        with open(path, 'w') as data_file:
            json.dump(self.data, data_file, sort_keys = True, indent = 4, ensure_ascii=False)

    def update_data(self):
        """
        Update the data for the programs run.
        """
        most_recent_data = { self.program_data["name"] : self.program_data["path"] }
        self.data["programs_run"].update(most_recent_data)
        self.write_program_file()

    def determine_stage_of_interaction(self, input_statement):
        """
        Determines at which point in the interaction with
        the user chatterbot is.
        """
        confidence = 0

        length = len(self.conversation)
        if length == 0:
            length = 1
        else:
            length += 1

        # Parsing through the conversation with chatterbot looking for information
        user_input = ""
        for conversation_index in range(0, length):
            if conversation_index == len(self.conversation):
                user_input = input_statement.text
            else:
                user_input = self.conversation[conversation_index][0]

            # Determining whether suggested path was asked
            if "previously_used" in self.stage:
                # @TODO: Replace the hardcoded "yes" with a call to a utility
                #   function that determines if any word similar to (in this
                #   case) "yes" is the text
                if input_statement.text.lower() == "yes":
                    self.stage = "name path"
                    self.program_data["path"] = self.program_data["suggested_path"]

                    return 1

            # Getting name of program (if available)
            extracted_name = self.extract_name(user_input)
            if self.program_data["name"] is "":
                if extracted_name is not "":
                    self.program_data["name"] = extracted_name
                    self.stage = "name"
            elif self.program_data["name"] is not extracted_name and extracted_name is not "":
                self.program_data["name"] = extracted_name
                self.stage = "name"

            # Getting path of program (if available)
            extracted_path = self.extract_path(user_input)
            if self.program_data["path"] is "":
                if extracted_path is not "":
                    self.program_data["path"] = extracted_path
                    self.stage += " path"
            elif self.program_data["path"] is not extracted_path and extracted_path is not "":
                self.program_data["path"] = extracted_path
                self.stage += " path"

        if self.stage != "":
            confidence = 1

        if self.stage is not "name path":
            # Read through the programs
            for program in self.data["programs_run"]:
                if self.program_data["name"] == program:
                    # Use a suggested path if the program has been used before
                    self.stage += " previously_used"
                    self.program_data["suggested_path"] = self.data["programs_run"][program]

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
        # @TODO: Implement more ways a user can communicate the name for
        #   a program
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
        # @TODO: Implement more ways a user can communicate the path for
        #   a program
        for word in self.tagger.tokenize(user_input):
            if "/" in word:
                if word.endswith("/"):
                    path = word
                else:
                    split = word.split("/")
                    path = "/".join(split[:len(split) - 1]) + "/"
                break

        return path
