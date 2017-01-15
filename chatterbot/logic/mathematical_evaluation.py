from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import re
import os
import json
import math
import decimal


class MathematicalEvaluation(LogicAdapter):
    """
    The MathematicalEvaluation logic adapter parses input to
    determine whether the user is asking a question that requires
    math to be done. If so, MathematicalEvaluation goes through a
    set of steps to parse the input and extract the equation that
    must be solved. The steps, in order, are:

    1) Normalize input: Remove punctuation and other irrelevant data
    2) Convert words to numbers
    3) Extract the equation
    4) Simplify the equation
    5) Solve the equation & return result
    """
    functions = {
        'sqrt': math.sqrt,

        # Most people assume a log of base 10 when a base is not specified
        'log': math.log10
    }

    def __init__(self, **kwargs):
        super(MathematicalEvaluation, self).__init__(**kwargs)

        language = kwargs.get('math_words_language', 'english')
        self.math_words = self.get_language_data(language)
        self.cache = {}

    def get_language_data(self, language):
        """
        Load language-specific data
        """
        from chatterbot.corpus import Corpus

        corpus = Corpus()

        math_words_data_file_path = corpus.get_file_path(
            'chatterbot.corpus.{}.math_words'.format(language),
            extension='json'
        )

        try:
            with open(math_words_data_file_path) as data:
                return json.load(data)
        except IOError:
            raise self.UnrecognizedLanguageException(
                'A math_words data file was not found for `{}` at `{}`.'.format(
                    language, math_words_data_file_path
                )
            )

    def can_process(self, statement):
        """
        Determines whether it is appropriate for this
        adapter to respond to the user input.
        """
        confidence, response = self.process(statement)
        self.cache[statement.text] = (confidence, response)
        return confidence == 1

    def process(self, statement):
        """
        Takes a statement string.
        Returns the simplified statement string
        with the mathematical terms solved.
        """
        input_text = statement.text

        # Use the result cached by the process method if it exists
        if input_text in self.cache:
            cached_result = self.cache[input_text]
            self.cache = {}
            return cached_result

        # Getting the mathematical terms within the input statement
        expression = str(self.simplify_chunks(self.normalize(input_text)))

        response = Statement(text=expression)

        try:
            response.text += '= ' + str(
                eval(expression, {f: self.functions[f] for f in self.functions})
            )

            # Replace '**' with '^' for evaluated exponents
            response.text = response.text.replace('**', '^')

            # The confidence is 1 if the expression could be evaluated
            response.confidence = 1
        except:
            response.confidence = 0

        return response.confidence, response

    def simplify_chunks(self, input_text):
        """
        Separates the incoming text.
        """
        string = ''
        chunks = re.split(r'([\w\.-]+|[\(\)\*\+])', input_text)
        chunks = [chunk.strip() for chunk in chunks]
        chunks = [chunk for chunk in chunks if chunk != '']

        classifiers = [
            'is_integer', 'is_float', 'is_operator', 'is_constant', 'is_function'
        ]

        for chunk in chunks:
            for classifier in classifiers:
                result = getattr(self, classifier)(chunk)
                if result is not False:
                    string += str(result) + ' '
                    break

        # Replace '^' with '**' to evaluate exponents
        string = string.replace('^', '**')

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

    def is_constant(self, string):
        """
        If the string is a mathematical constant, returns
        said constant. Otherwise, it returns False.
        """
        constants = {
            'pi': 3.141693,
            'e': 2.718281
        }
        return constants.get(string, False)

    def is_function(self, string):
        """
        If the string is an availbale mathematical function, returns
        said function. Otherwise, it returns False.
        """
        if string in self.functions:
            return string
        else:
            return False

    def is_operator(self, string):
        """
        If the string is an operator, returns
        said operator. Otherwise, it returns false.
        """
        if string in '+-/*^()':
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

    def substitute_words(self, string):
        """
        Substitutes numbers for words.
        """
        condensed_string = '_'.join(string.split())

        for word in self.math_words['words']:
            condensed_string = re.sub(
                '_'.join(word.split(' ')),
                self.math_words['words'][word],
                condensed_string
            )

        for number in self.math_words['numbers']:
            condensed_string = re.sub(
                number,
                str(self.math_words['numbers'][number]),
                condensed_string
            )

        for scale in self.math_words['scales']:
            condensed_string = re.sub(
                '_' + scale,
                ' ' + self.math_words['scales'][scale],
                condensed_string
            )

        condensed_string = condensed_string.split('_')
        for chunk_index in range(0, len(condensed_string)):
            value = ''

            try:
                value = str(eval(condensed_string[chunk_index]))

                condensed_string[chunk_index] = value
            except:
                pass

        for chunk_index in range(0, len(condensed_string)):
            condensed_chunk = condensed_string[chunk_index]
            if self.is_integer(condensed_chunk) or self.is_float(condensed_chunk):
                i = 1
                start_index = chunk_index
                end_index = -1
                while (chunk_index + i < len(condensed_string) and (self.is_integer(condensed_string[chunk_index + i]) or self.is_float(condensed_string[chunk_index + i]))):
                    end_index = chunk_index + i
                    i += 1

                for sub_chunk in range(start_index, end_index):
                    condensed_string[sub_chunk] += ' +'

                condensed_string[start_index] = '( ' + condensed_string[start_index]
                condensed_string[end_index] += ' )'

        return ' '.join(condensed_string)

    class UnrecognizedLanguageException(Exception):
        """
        Exception raised when the specified language is not known.
        """
        pass
