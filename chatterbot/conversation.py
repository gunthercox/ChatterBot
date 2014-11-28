class Statement(object):
    """
    A statement is a single expression declared by a source such as a person.
    """

    def __init__(self, name, text, date=None, sentiment=None):

        if not date:
            import datetime
            self.date = datetime.datetime.now()

        if type(date) is str:
            import datetime
            #      'Jun 1 2005  1:33PM'
            #date_format = '%b %d %Y %I:%M%p'
            #self.date = datetime.datetime.strptime(date, date_format)
            pass

        self.name = name
        self.date = date
        self.text = text
        self.sentiment = sentiment

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
                for line in lines:
                    user, date, text = line

                    # Make sure the text is a string and not an integer or other type
                    text = str(text)

                    statement = Statement(user, text, date=date)
                    self.add(statement)

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

    def find_closest_response(self, text):
        """
        Returns the statement after the closest matchng statement in the
        conversation.
        """
        from fuzzywuzzy import fuzz

        closest_statement = None
        closest_ratio = 0
        response = []

        for statement in self.statements:
            ratio = fuzz.ratio(statement.text, text)
            if ratio > closest_ratio:
                closest_statement = statement
                closest_ratio = ratio

                '''
                If the closest match is not the last one in the conversation,
                then return the next line as the response.
                '''
                index = self.statements.index(statement)

                if index + 1 < len(self):
                    response = []
                    response.append(self.statements[index + 1])
    
                    '''
                    if the next line exists and has the same user as the first
                    response, then add that one to the list.
                    '''
                    #TODO

        return response, closest_ratio

    def get_sentiment(user):
        """
        Returns the average sentament for a single user throughout a
        conversation.
        """
        sentiment = []
        for statement in self.statements:
            if statement.user == user:
                sentiment.append(statement)

        return "" #TODO: return the average sentiment
