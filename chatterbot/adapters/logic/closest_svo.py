from .logic import LogicAdapter

from regex4dummies import Toolkit


class ClosestSVOAdapter(LogicAdapter):

    def __init__(self):
        super(ClosestSVOAdapter, self).__init__()


    def get_dependencies(self, text):
        """
        Takes a string and converts it to its
        dependecies separated in a list
        """
        dependences = []

        return dependencies


    def get_similarity(self, string1, string2):
        """
        Calculate the similarity of two statements.
        This is based on the total similarity between
        each word in each sentence.
        """
        import re

        # Instantiating variables
        similarity_tester = Toolkit()
        similarity = 0

        # Getting the dependencies of the strings
        dependencies1 = similarity_tester.find_dependencies( text=string1, parser='pattern', response_type='simplified' )
        dependencies2 = similarity_tester.find_dependencies( text=string2, parser='pattern', response_type='simplified' )

        # Comparing the dependencies & generating similarity
        if dependencies1[ 0 ] == dependencies2[ 0 ]:
            similarity += 1

        if dependencies1[ 1 ] == dependencies2[ 1 ]:
            similarity += 1

        if dependencies1[ 2 ] == dependencies2[ 2 ]:
            similarity += 1

        # Returning the found similarity
        return similarity


    def get(self, text, list_of_statements):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        # Check if there is no options
        if not list_of_statements:
            return text

        # Check if an exact match exists
        if text in list_of_statements:
            return text

        closest_statement = list_of_statements[0]
        closest_similarity = 0

        # For each option in the list of options
        for statement in list_of_statements:
            similarity = self.get_similarity(text, statement)

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_statement = statement

        return closest_statement
