from .plugin import PluginAdapter
import re
import os, json
import decimal

class EvaluateMathematically(PluginAdapter):

    def should_answer(self, input_text):
        """
        Determines whether it is appropriate for this plugin
        to respond to the user input.
        """

        response = self.process( input_text )

        if response is False:
            return False
        else:
            return True


    def process(self, input_text):
        """
        Takes a statement string.
        Returns the simplified statement string
        with the mathematical terms "solved".
        """

        # Getting the mathematical terms within the input statement
        expression = self.simplify_chunks( self.normalize( input_text ) )

        # Returning important information
        try:
            expression += '= ' + str( eval( expression ) )

            return expression
        except:
            return False


    def simplify_chunks(self, input_text):
        """
        Separates the incoming text.
        """

        string = ''

        for chunk in input_text.split():

            is_chunk_integer = self.is_integer( chunk )

            if is_chunk_integer is False:
                is_chunk_float = self.is_float( chunk )

                if is_chunk_float is False:
                    is_chunk_operator = self.is_operator( chunk )

                    if not is_chunk_operator is False:
                        string += str( is_chunk_operator ) + ' '
                else:
                    string += str( is_chunk_float ) + ' '
            else:
                string += str( is_chunk_integer ) + ' '

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
            return int( string )
        except:
            return False


    def is_operator(self, string):
        """
        If the string is an operator, returns
        said operator. Otherwise, it returns
        false.
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
        if len( string ) is 0:
            return string

        # Setting all words to lowercase
        string = string.lower()

        # Removing punctuation
        if not string[-1].isalnum():
            string = string[ : -1 ]

        # Removing words
        string = self.substitute_words( string )

        # Returning normalized text
        return string

    def load_data( self, language ):
        """
        Load language-specific data
        """

        if language == "english":
            with open(os.path.join(os.path.dirname(__file__), 'data', "math_words_EN.json")) as data_file:
                data = json.load(data_file)
            self.data = data


    def substitute_words(self, string):
        """
        Substitutes numbers for words.
        """

        self.load_data( "english" )

        condensed_string = '_'.join( string.split() )

        for word in self.data[ "words" ]:
            condensed_string = re.sub( '_'.join( word.split( ' ' ) ), self.data[ "words" ][ word ], condensed_string )

        for number in self.data[ "numbers" ]:
            condensed_string = re.sub( number, str( self.data[ "numbers" ][ number ] ), condensed_string )

        for scale in self.data[ "scales" ]:
            condensed_string = re.sub( "_" + scale, " " + self.data[ "scales" ][ scale ], condensed_string)

        condensed_string = condensed_string.split( '_' )
        for chunk_index in range( 0, len( condensed_string ) ):
            value = ""

            try:
                value = str( eval( condensed_string[ chunk_index ] ) )

                condensed_string[ chunk_index ] = value
            except:
                pass

        for chunk_index in range( 0, len( condensed_string ) ):
            if self.is_integer( condensed_string[ chunk_index ] ) or self.is_float( condensed_string[ chunk_index ] ):
                i = 1
                start_index = chunk_index
                end_index = -1
                while( chunk_index + i < len( condensed_string ) and ( self.is_integer( condensed_string[ chunk_index + i ] ) or self.is_float( condensed_string[ chunk_index + i ] ) ) ):
                    end_index = chunk_index + i
                    i += 1

                for sub_chunk in range( start_index, end_index ):
                    condensed_string[ sub_chunk ] += " +"

                condensed_string[ start_index ] = "( " + condensed_string[ start_index ]
                condensed_string[ end_index ] += " )"

        return ' '.join( condensed_string )
