from .preprocessor import PreProcessorAdapter
import re
import os, json

class EvaluateMathematically(PreProcessorAdapter):

    def process(self, input_text):
        """
        Takes a statement string.
        Returns the simplified statement string
        with the mathematical terms "solved".
        """

        # Getting the mathematical terms within the input statement
        expression, string = self.simplify_chunks( self.normalize( input_text ) )

        # Returning important information
        try:
            string += '= ' + str( eval( string ) )#self.evaluate( string ) )

            return string, True
        except:
            return string, False


    def simplify_chunks(self, input_text):
        """
        Separates the incoming text.
        """

        expression = []
        string = ''

        for chunk in input_text.split( ' ' ):

            is_integer = self.isInteger( chunk )

            if is_integer == False:
                is_float = self.isFloat( chunk )

                if is_float == False:
                    is_operator = self.isOperator( chunk )

                    if is_operator == False:
                        continue
                    else:
                        expression.append( is_operator )

                        string += str( is_operator ) + ' '
                else:
                    expression.append( is_float )

                    string += str( is_float ) + ' '
            else:
                expression.append( is_integer )

                string += str( is_integer ) + ' '

        return expression, string


    def evaluate( self, expression ):
        """
        Evaluates a set of expressions
        and produces an answer. Then,
        it returns the answer.
        """

        return eval( expression )


    def isFloat(self, string):
        """
        If the string is a float, returns
        the float of the string. Otherwise,
        it returns False.
        """

        try:
            float( integer )

            return float( integer );
        except:
            return False


    def isInteger(self, string):
        """
        If the string is an integer, returns
        the int of the string. Otherwise,
        it returns False.
        """

        if string.isdigit():
            return int( string )
        else:
            return False


    def isOperator(self, string):
        """
        If the string is an operator, returns
        said operator. Otherwise, it returns
        false.
        """

        if string in "+-/*^\(\)":
            return string
        else:
            return False


    def normalize(self, string):
        """
        Normalizes input text, reducing errors
        and improper calculations.
        """

        # Setting all words to lowercase
        string = string.lower()

        # Removing punctuation
        string = re.sub( '[.!?/:;]', '', string )

        # Removing words
        string = self.substitute_words( string )

        # Returning normalized text
        return string

    def load_data( self, language ):
        """
        Load language-specific data
        """

        if language == "english":
            with open(os.path.join(os.path.dirname(__file__), 'data') + "/math_words_EN.json") as data_file:
                data = json.load(data_file)
            self.data = data


    def substitute_words(self, string):
        """
        Substitutes numbers for words.
        """

        self.load_data( "english" )

        condensed_string = '_'.join( string.split( ' ' ) )

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
            if self.isInteger( condensed_string[ chunk_index ] ) or self.isFloat( condensed_string[ chunk_index ] ):
                i = 1
                start_index = chunk_index
                end_index = -1
                while( chunk_index + i < len( condensed_string ) and ( self.isInteger( condensed_string[ chunk_index + i ] ) or self.isFloat( condensed_string[ chunk_index + i ] ) ) ):
                    end_index = chunk_index + i
                    i += 1

                for sub_chunk in range( start_index, end_index ):
                    condensed_string[ sub_chunk ] += " +"

                condensed_string[ start_index ] = "( " + condensed_string[ start_index ]
                condensed_string[ end_index ] += " )"

        return ' '.join( condensed_string )
