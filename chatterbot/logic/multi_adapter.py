from __future__ import unicode_literals
from collections import Counter
from chatterbot import utils
from .logic_adapter import LogicAdapter


class MultiLogicAdapter(LogicAdapter):
    """
    MultiLogicAdapter allows ChatterBot to use multiple logic
    adapters. It has methods that allow ChatterBot to add an
    adapter, set the chat bot, and process an input statement
    to get a response.
    """

    def __init__(self, **kwargs):
        super(MultiLogicAdapter, self).__init__(**kwargs)

        # Logic adapters added by the chat bot
        self.adapters = []

        # Required logic adapters that must always be present
        self.system_adapters = []

    def get_initialization_functions(self):
        """
        Get the initialization functions for each logic adapter.
        """
        functions_dict = {}

        # Iterate over each adapter and get its initialization functions
        for logic_adapter in self.get_adapters():
            functions = logic_adapter.get_initialization_functions()
            functions_dict.update(functions)

        return functions_dict

    def process(self, statement):
        """
        Returns the output of a selection of logic adapters
        for a given input statement.

        :param statement: The input statement to be processed.
        """
        results = []
        result = None
        max_confidence = -1

        for adapter in self.get_adapters():
            if adapter.can_process(statement):

                output = adapter.process(statement)
                results.append((output.confidence, output, ))

                self.logger.info(
                    '{} selected "{}" as a response with a confidence of {}'.format(
                        adapter.class_name, output.text, output.confidence
                    )
                )

                if output.confidence > max_confidence:
                    result = output
                    max_confidence = output.confidence
            else:
                self.logger.info(
                    'Not processing the statement using {}'.format(adapter.class_name)
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

        result.confidence = max_confidence
        return result

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

    def get_adapters(self):
        """
        Return a list of all logic adapters being used, including system logic adapters.
        """
        adapters = []
        adapters.extend(self.adapters)
        adapters.extend(self.system_adapters)
        return adapters

    def add_adapter(self, adapter, **kwargs):
        """
        Appends a logic adapter to the list of logic adapters being used.

        :param adapter: The logic adapter to be added.
        :type adapter: `LogicAdapter`
        """
        utils.validate_adapter_class(adapter, LogicAdapter)
        adapter = utils.initialize_class(adapter, **kwargs)
        self.adapters.append(adapter)

    def insert_logic_adapter(self, logic_adapter, insert_index, **kwargs):
        """
        Adds a logic adapter at a specified index.

        :param logic_adapter: The string path to the logic adapter to add.
        :type logic_adapter: str

        :param insert_index: The index to insert the logic adapter into the list at.
        :type insert_index: int
        """
        utils.validate_adapter_class(logic_adapter, LogicAdapter)

        NewAdapter = utils.import_module(logic_adapter)
        adapter = NewAdapter(**kwargs)

        self.adapters.insert(insert_index, adapter)

    def remove_logic_adapter(self, adapter_name):
        """
        Removes a logic adapter from the chat bot.

        :param adapter_name: The class name of the adapter to remove.
        :type adapter_name: str
        """
        for index, adapter in enumerate(self.adapters):
            if adapter_name == type(adapter).__name__:
                del self.adapters[index]
                return True
        return False

    def set_chatbot(self, chatbot):
        """
        Set the chatbot for each of the contained logic adapters.
        """
        super(MultiLogicAdapter, self).set_chatbot(chatbot)

        for adapter in self.get_adapters():
            adapter.set_chatbot(chatbot)
