from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
import re
import os
import json
import decimal


class EvaluateMathematically(LogicAdapter):
    """
    The EvaluateMathematically logic adapter parses input to
    determine whether the user is asking a question that requires
    math to be done. If so, EvaluateMathematically goes through a
    set of steps to parse the input and extract the equation that
    must be solved. The steps, in order, are:

    1) Normalize input: Remove punctuation and other irrelevant data
    2) Convert words to numbers
    3) Extract the equation
    4) Simplify the equation
    5) Solve the equation & return result
    """

    def can_process(self, statement):
        """
        Determines whether it is appropriate for this
        adapter to respond to the user input.
        """
        confidence, response = self.process(statement)
        return confidence == 1

    def process(self, statement):
        """
        Takes a statement string.
        Returns the simplified statement string
        with the mathematical terms "solved".
        """
        input_text = statement.text

        # Getting the mathematical terms within the input statement
        expression = str(self.simplify_chunks(self.normalize(input_text)))

        # Returning important information
        try:
            expression += "= " + str(eval(expression))

            # return a confidence of 1 if the expression could be evaluated
            return 1, Statement(expression)
        except:
            return 0, Statement(expression)

    def simplify_chunks(self, input_text):
        """
        Separates the incoming text.
        """
        string = ''

        for chunk in input_text.split():

            is_chunk_integer = self.is_integer(chunk)

            if is_chunk_integer is False:
                is_chunk_float = self.is_float(chunk)

                if is_chunk_float is False:
                    is_chunk_operator = self.is_operator(chunk)

                    if is_chunk_operator is not False:
                        string += str(is_chunk_operator) + ' '
                else:
                    string += str(is_chunk_float) + ' '
            else:
                string += str(is_chunk_integer) + ' '

        return string

    def is_float(self, string):
        """
        If the string is a float, returns
        the float of the string. Otherwise,
        it returns False.
        """
        try:
            return decimal.Decimal(string)
        except decimal.DecimalException:
            return False

    def is_integer(self, string):
        """
        If the string is an integer, returns
        the int of the string. Otherwise,
        it returns False.
        """
        try:
            return int(string)
        except:
            return False

    def is_operator(self, string):
        """
        If the string is an operator, returns
        said operator. Otherwise, it returns false.
        """
        if string in "+-/*^()":
            return string
        else:
            return False

    def normalize(self, string):
        """
        Normalizes input text, reducing errors
        and improper calculations.
        """

        # If the string is empty, just return it
        if len(string) is 0:
            return string

        # Setting all words to lowercase
        string = string.lower()

        # Removing punctuation
        if not string[-1].isalnum():
            string = string[:-1]

        # Removing words
        string = self.substitute_words(string)

        # Returning normalized text
        return string

    def load_data(self, language):
        """
        Load language-specific data
        """
        if language == "english":
            data_file = os.path.join(
                os.path.dirname(__file__), 'data', 'math_words_EN.json'
            )
            with open(data_file) as data_file:
                data = json.load(data_file)
            self.data = data

    def substitute_words(self, string):
        """
        Substitutes numbers for words.
        """
        self.load_data("english")

        condensed_string = '_'.join(string.split())

        for word in self.data["words"]:
            condensed_string = re.sub(
                '_'.join(word.split(' ')),
                self.data["words"][word],
                condensed_string
            )

        for number in self.data["numbers"]:
            condensed_string = re.sub(
                number,
                str(self.data["numbers"][number]),
                condensed_string
            )

        for scale in self.data["scales"]:
            condensed_string = re.sub(
                "_" + scale,
                " " + self.data["scales"][scale],
                condensed_string
            )

        condensed_string = condensed_string.split('_')
        for chunk_index in range(0, len(condensed_string)):
            value = ""

            try:
                value = str(eval(condensed_string[chunk_index]))

                condensed_string[chunk_index] = value
            except:
                pass

        for chunk_index in range(0, len(condensed_string)):
            if self.is_integer(condensed_string[chunk_index]) or self.is_float(condensed_string[chunk_index]):
                i = 1
                start_index = chunk_index
                end_index = -1
                while (chunk_index + i < len(condensed_string) and (self.is_integer(condensed_string[chunk_index + i]) or self.is_float(condensed_string[chunk_index + i]))):
                    end_index = chunk_index + i
                    i += 1

                for sub_chunk in range(start_index, end_index):
                    condensed_string[sub_chunk] += " +"

                condensed_string[start_index] = "( " + condensed_string[start_index]
                condensed_string[end_index] += " )"

        return ' '.join(condensed_string)
