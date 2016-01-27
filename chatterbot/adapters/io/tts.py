from chatterbot.adapters.io import IOAdapter
from chatterbot.utils.read_input import input_function

import os
import platform
import subprocess


class MacOSXTTS(IOAdapter):

    def process_input(self):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return user_input

    def process_response(self, statement):
        """
        Speak the response.
        """
        cmd = ['say', str(statement.text)]
        if platform.system().lower() == 'darwin':
            subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return statement.text
