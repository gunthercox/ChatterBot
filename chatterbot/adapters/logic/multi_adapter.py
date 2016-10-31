from .logic_adapter import LogicAdapter
from collections import Counter


class MultiLogicAdapter(LogicAdapter):
    """
    MultiLogicAdapter allows ChatterBot to use multiple logic
    adapters. It has methods that allow ChatterBot to add an
    adapter, set the context, and process an input statement
    to get a response.
    """

    def __init__(self, **kwargs):
        super(MultiLogicAdapter, self).__init__(**kwargs)

        self.adapters = []

    def process(self, statement):
        """
        Returns the outout of a selection of logic adapters
        for a given input statement.

        :param statement: The input statement to be processed.
        """
        results = []
        result = None
        max_confidence = -1

        for adapter in self.adapters:
            if adapter.can_process(statement):
                confidence, output = adapter.process(statement)
                results.append((confidence, output, ))

                self.logger.info(
                    u'{} selected "{}" as a response with a confidence of {}'.format(
                         str(adapter.__class__), output.text, confidence
                    )
                )

                if confidence > max_confidence:
                    result = output
                    max_confidence = confidence
            else:
                self.logger.info(
                    u'Not processing the statement using {}'.format(
                        str(adapter.__class__)
                    )
                )

        # If multiple adapters agree on the same statement,
        # then that statement is more likely to be the correct response
        if len(results) >= 3:
            statements = [s[1] for s in results]
            count = Counter(statements)
            most_common = count.most_common()
            if most_common[0][1] > 1:
                result = most_common[0][0]
                max_confidence = self.get_greatest_confidence(result, results)

        return max_confidence, result

    def get_greatest_confidence(self, statement, options):
        """
        Returns the greatest confidence value for a statement that occurs
        multiple times in the set of options.

        :param statement: A statement object.
        :param options: A tuple in the format of (confidence, statement).
        """
        values = []
        for option in options:
            if option[1] == statement:
                values.append(option[0])

        return max(values)

    def add_adapter(self, adapter):
        """
        Appends a logic adapter to the list of logic adapters being used.

        :param adapter: The logic adapter to be added.
        :type adapter: LogicAdapter
        """
        self.adapters.append(adapter)

    def set_context(self, context):
        """
        Set the context for each of the contained logic adapters.
        """
        super(MultiLogicAdapter, self).set_context(context)

        for adapter in self.adapters:
            adapter.set_context(context)
