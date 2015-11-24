from evaluate_mathematically import EvaluateMathematically

class PluginChooser():

    def __init__( self, **kwargs ):
        """
        Initializes all plugins & initial variables.
        """

        self.plugins = [
            EvaluateMathematically(**kwargs)
        ]


    def choose( self, input_statement ):
        """
        Used to determine whether a plugin should be used
        to "answer" or reply to the user input.
        """

        # Testing each plugin to determine whether it should be used to answer user input
        for plugin in self.plugins:
            should_use = plugin.should_answer( input_statement.text )

            if should_use:
                return plugin.process( input_statement.text )

        return False
