from .logic_adapter import LogicAdapter
from concurrent.futures import ThreadPoolExecutor


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

    def get_usable_adapters(self, statement):
        usable_adapters = []

        for adapter in self.adapters:
            if adapter.can_process(statement):
                usable_adapters.append([adapter, statement])
            else:
                self.logger.info(
                    u'Not processing the statement using {}'.format(
                        str(adapter.__class__)
                    )
                )

        return usable_adapters

    def execute_adapter_process(self, values):
        adapter = values[0]
        statement = values[1]

        confidence, output = adapter.process(statement)

        return confidence, output, adapter

    def process(self, statement):
        """
        Returns the outout of a selection of logic adapters
        for a given input statement.

        :param statement: The input statement to be processed.
        """
        result = None
        max_confidence = -1

        usable_adapters = self.get_usable_adapters(statement)

        # with ProcessPoolExecutor(max_executors) as executor:
        with ThreadPoolExecutor(max_workers=len(usable_adapters)) as executor:
            for confidence, output, adapter in executor.map(self.execute_adapter_process, usable_adapters):

                self.logger.info(
                    u'{} selected "{}" as a response with a confidence of {}'.format(
                         str(adapter.__class__), output.text, confidence
                    )
                )

                if confidence > max_confidence:
                    result = output
                    max_confidence = confidence

        return max_confidence, result

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
