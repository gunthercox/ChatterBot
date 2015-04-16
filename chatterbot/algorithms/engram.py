class Engram(object):

    def __init__(self, statement, database):
        """
        Constructor for the Engram object takes a statement that
        exists within the database, and the database object.
        """

        if not statement in database:
            raise Exception("A matching statement must exist in the database")

        self.statement = statement
        self.database = database

    def get_occurrence_count(self, key, database):
        """
        Return the number of times a statement occurs in the database
        """

        if "occurrence" in database[key]:
            return database[key]["occurrence"]

        # If the number of occurances has not been set then return 1
        return 1

    def responces_in_database(self, statement):
        """
        Returns true if a given statement is in the database.
        Otherwise, returns false
        """

        # Check if the statement has responses in the database
        if "in_response_to" in self.database[statement] and \
            self.statement in self.database[statement]["in_response_to"]:
            return True

        return False

    def keys(self):
        """
        Returns a statement in response to the closest matching statement in
        the database. For each match, the statement with the greatest number
        of occurrence will be returned.
        """

        # Initialize the matching responce with the first statement in the database
        # The list of keys has to be cast as a list for python 3
        matching_response = list(self.database[0].keys())[0]
        occurrence_count = self.get_occurrence_count(matching_response, self.database)

        for statement in self.database:

            if self.responces_in_database(statement):

                statement_occurrence_count = self.get_occurrence_count(statement, self.database)

                # Keep the more common statement
                if statement_occurrence_count >= occurrence_count:
                    matching_response = statement
                    occurrence_count = statement_occurrence_count

                #TODO? If the two statements occure equaly in frequency, should we keep one at random

        # Choose the most common selection of matching response
        return {matching_response: self.database[matching_response]}
