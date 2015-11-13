from .preprocessor import PreProcessorAdapter
import re

class EvaluateMathematically(PreProcessorAdapter):

    def process(self, input_text):
        """
        Takes a statement string.
        Returns the simplified statement string
        with the mathematical terms "solved".
        """

        #input_text = re.sub( '.', '', input_text )

        expression = self.simplify_chunks( input_text )

        print input_text

        return input_text


    def simplify_chunks(self, input_text):
        """
        Separates the incoming text.
        """

        expression = []

        for chunk in input_text.split( ' ' ):
            is_integer = self.isInteger( chunk )

            if is_integer == False:
                is_float = self.isFloat( chunk )

                if is_float == False:
                    continue
                else:
                    expression.append( is_float )
            else:
                expression.append( is_integer )


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

        if string in "+-/*^":
            return string
        else:
            return False
