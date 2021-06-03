from chatterbot.logic import LogicAdapter


class WikipediaResponseAdapter(LogicAdapter):
    """
    Return a response which get from Wikipedia.

    :kwargs:
        * *lang_code* (``str``) --
          Decide which language you want to get answers from Wikipedia.
          The default is English Wikipedia.
        * *cut_threshold* (``int``) --
          If the data from Wikipedia is too long,
          it's the minimum length to cut. The standard is dot character.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.lang_code = kwargs.get('lang_code', 'en')
        self.cut_threshold = kwargs.get('cut_threshold', 2)
        self.input_text = ''
        self.input_search_text = ''
        self.find_word = ''
        self.response_statement = ''

    def can_process(self, statement):
        if not self.lang_code:
            return False

        input_search_text = statement.search_text \
            if statement.search_text else \
            self.chatbot.storage.tagger.get_text_index_string(statement.text)

        for props in input_search_text.split(' '):
            props_list = props.split(':')
            if props_list[0] == "VERB":
                self.find_word = props_list[1]
                break

        if not self.find_word:
            return False

        from requests import get

        url = 'https://' + self.lang_code + '.wikipedia.org/w/api.php'

        query = '?format=json&action=query&prop=extracts' \
                + '&exlimit=1&explaintext&exintro&titles=' \
                + self.find_word \
                + '&redirects=true'

        response = get(url=(url + query)).json()

        pages = response['query']['pages']

        if '-1' in pages.keys():
            return False

        key = next(iter(pages.keys()))
        self.input_text = statement.text
        self.input_search_text = input_search_text

        response_text = pages[key]['extract']

        cut_response = response_text.split('.')

        if self.cut_threshold < len(cut_response):
            self.response_statement = ''
            for i in range(self.cut_threshold):
                self.response_statement += cut_response[i] + '.'
        else:
            self.response_statement = response_text

        self.response_statement = \
            self.response_statement.replace('\n', ' ')

        return True

    def process(self, statement,
                additional_response_selection_parameters=None):
        from chatterbot.conversation import Statement

        output_search_text = self.chatbot.storage.tagger.get_text_index_string(
            self.response_statement)

        response_text = Statement(
            text=self.response_statement,
            in_response_to=statement.text,
            search_text=output_search_text,
            search_in_respond_to=self.input_search_text,
        )

        if statement.text == self.input_text:
            response_text.confidence = 1
        else:
            response_text.confidence = 0

        return response_text
