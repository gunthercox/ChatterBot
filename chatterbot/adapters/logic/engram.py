from .logic import LogicAdapter


class EngramAdapter(LogicAdapter):

    def __init__(self, database):
        """
        Constructor for the Engram object takes a statement that
        exists within the database, and the database object.
        """

        self.database = database

    def get_occurrence_count(self, key):
        """
        Return the number of times a statement occurs in the database
        """

        statement = self.database.find(key)

        if "occurrence" in statement:
            return statement["occurrence"]

        # If the number of occurences has not been set then return 1
        return 1

    def responces_in_database(self, statement, entry):
        """
        Returns true if a given statement is in the database.
        Otherwise, returns false
        """

        statement = self.database.find(statement)

        # Check if the statement has responses in the database
        if "in_response_to" in statement and entry in statement["in_response_to"]:
            return True

        return False

    def get(self, input_statement):
        """
        Returns a statement in response to the closest matching statement in
        the database. For each match, the statement with the greatest number
        of occurrence will be returned.
        """

        if not input_statement in self.database.keys():
            raise Exception("A matching statement must exist in the database")

        # Initialize the matching responce with the first statement in the database
        matching_response = self.database.keys()[0]
        occurrence_count = self.get_occurrence_count(matching_response)

        for statement in self.database.keys():

            if self.responces_in_database(statement, input_statement):

                statement_occurrence_count = self.get_occurrence_count(statement)

                # Keep the more common statement
                if statement_occurrence_count >= occurrence_count:
                    matching_response = statement
                    occurrence_count = statement_occurrence_count

                #TODO? If the two statements occure equaly in frequency, should we keep one at random

        # Choose the most common selection of matching response
        return {matching_response: self.database.find(matching_response)}
