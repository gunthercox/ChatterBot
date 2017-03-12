# -*- coding: utf-8 -*-
import tkinter as tk
try:
    import ttk as ttk
    import ScrolledText
except ImportError:
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText
import time

from chatterbot import ChatBot

class TkinterGUIExample(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Create & set window variables.
        """
        tk.Tk.__init__(self, *args, **kwargs)

        self.chatbot = ChatBot("No Output",
            storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ],
            input_adapter="chatterbot.input.VariableInputTypeAdapter",
            output_adapter="chatterbot.output.OutputAdapter",
            database="../database.db"
        )

        self.title("Chatterbot")

        self.initialize()

    def initialize(self):
        """
        Set window layout.
        """
        self.grid()

        self.respond = ttk.Button(self, text='Get Response', command=self.get_response)
        self.respond.grid(column=0, row=0, sticky='nesw', padx=3, pady=3)

        self.usr_input = ttk.Entry(self, state='normal')
        self.usr_input.grid(column=1, row=0, sticky='nesw', padx=3, pady=3)

        self.conversation_lbl = ttk.Label(self, anchor=tk.E, text='Conversation:')
        self.conversation_lbl.grid(column=0, row=1, sticky='nesw', padx=3, pady=3)

        self.conversation = ScrolledText.ScrolledText(self, state='disabled')
        self.conversation.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=3, pady=3)

    def get_response(self):
        """
        Get a response from the chatbot and display it.
        """
        user_input = self.usr_input.get()
        self.usr_input.delete(0, tk.END)

        response = self.chatbot.get_response(user_input)

        self.conversation['state'] = 'normal'
        self.conversation.insert(
            tk.END, "Human: " + user_input + "\n" + "ChatBot: " + str(response.text) + "\n"
        )
        self.conversation['state'] = 'disabled'

        time.sleep(0.5)

gui_example = TkinterGUIExample()
gui_example.mainloop()
