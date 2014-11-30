class Statement(object):
    """
    A statement is a single expression declared by a source such as a person.
    A statement may consist of a single or multiple sentences.
    """

    def __init__(self, name, text, date=None, sentiment=None):

        self.name = name
        self.date = date
        self.text = text
        self.response_to = None
        self.sentiment = sentiment

        if not date:
            import datetime
            self.date = datetime.datetime.now()

        # convert date strings to a date object
        if type(date) is str:
            import datetime
            date_format = "%Y-%m-%d-%H-%M-%S"

            # Get the date object if possible
            try:
                self.date = datetime.datetime.strptime(date, date_format)
            except ValueError:
                self.date = datetime.datetime.now()

    def __str__(self):
        return self.text

    def __iter__(self):
        dictionary = {
            "name": self.name,
            "date": str(self.date),
            "text": self.text
        }

        for key in dictionary:
            yield (key, dictionary[key])

    def update_timestamp(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        import datetime
        self.date = datetime.datetime.now().strftime(fmt)

    def set_name(self, name):
        self.name = name

    def in_response_to(self, previous_statement):
        """
        Setter method that takes a previous statement as a parameter.
        This allows the current object to be a response to the a previous
        statement.
        """
        self.response_to = previous_statement

    def detect_sentiment():
        """
        A property that describes hows the 
        """

        if self.sentiment:
            return self.sentiment

        # Evaluate the sentiment of the statement
        #else:
            # Would this be better done from the conversation level?
            


class Conversation(object):
    """
    A conversation is an ordered set of statements from which
    important trends in topics and attitudes can be identified.
    """

    def __init__(self):
        self.statements = []

    def __len__(self):
        """
        Returns the number of statements in the conversation.
        """
        return len(self.statements)

    def __iter__(self):
        """
        Allows the conversation to be iterable.
        """
        for statement in self.statements:
            yield statement

    def read(self, path):
        """
        Reads a conversation from a file.
        Loads each statement from the file into the conversation.
        """
        import os, csv

        # Continue only if the file is not empty
        if os.stat(path).st_size > 0:

            log = open(path, "r")
            lines = list(csv.reader(log))

            # Continue only if the file contains lines
            if lines:
                previous_statement = None
                for line in lines:
                    user, date, text = line

                    # Make sure the text is a string and not an integer or other type
                    text = str(text)

                    statement = Statement(user, text, date=date)
                    statement.in_response_to(previous_statement)
                    self.add(statement)

                    previous_statement = statement

    def write(self):
        """
        Saves the current conversation to a file
        """
        # TODO
        pass

    def add(self, statement):

        # Only add the statement if it contains valid text
        if statement.text.strip():
            self.statements.append(statement)

    def get(self, quantity):
        """
        Return the last n lines from the conversation.
        The number of lines returned is specified by the quantity variable.
        """

        # If length of lines is less than quantity return the lines that exist
        if quantity > len(self.statements):
            return self.statements

        # Return the last n statements
        quantity *= -1
        return self.statements[quantity:]

    def next_line(self, index):
        """
        If the closest match is not the last one in the conversation,
        then return the next line as the response.
        """

        index = index + 1

        if index >= len(self):
            return None, index

        return self.statements[index], index

    def find_closest_response(self, text):
        """
        Returns the statement after the closest matchng statement in the
        conversation.
        """
        from fuzzywuzzy import fuzz
        import random

        closest_ratio = 0
        response = []

        for statement in self:
            ratio = fuzz.ratio(statement.text, text)
            if ratio > closest_ratio:
                closest_ratio = ratio
                response = []

                index = self.statements.index(statement)

                '''
                If the next line exists and has the same user as the first
                response, then add that one to the list.
                '''
                next, index = self.next_line(index)
                while (not response and next) or (next and next.name == response[0].name):
                    response.append(next)
                    next, index = self.next_line(index)

            # If the ratios are the same, pick the one to keep at random
            elif ratio == closest_ratio and closest_ratio != 0:

                # Use a random boolean to determine which statement to keep
                if bool(random.getrandbits(1)):
                    response = []

                    index = self.statements.index(statement)

                    '''
                    If the next line exists and has the same user as the first
                    response, then add that one to the list.
                    '''
                    next, index = self.next_line(index)
                    while (not response and next) or (next and next.name == response[0].name):
                        response.append(next)
                        next, index = self.next_line(index)

        return response, closest_ratio

    def get_sentiment(name):
        """
        Returns the average sentament for a single user throughout a
        conversation.
        """
        sentiment = []
        for statement in self:
            if statement.name == name:
                sentiment.append(statement)

        return "" #TODO: return the average sentiment
