"""Python library allowing interaction with the Cleverbot API."""
import hashlib
import urllib
import urllib2


class Cleverbot:
    """
    Wrapper over the Cleverbot API.
    """
    HOST = "www.cleverbot.com"
    PROTOCOL = "http://"
    RESOURCE = "/webservicemin"
    API_URL = PROTOCOL + HOST + RESOURCE

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Accept-Language': 'en-us,en;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'no-cache',
        'Host': HOST,
        'Referer': PROTOCOL + HOST + '/',
        'Pragma': 'no-cache'
    }

    def __init__(self):
        """ The data that will get passed to Cleverbot's web API """
        self.data = {
            'stimulus': '',
            'start': 'y',  # Never modified
            'sessionid': '',
            'vText8': '',
            'vText7': '',
            'vText6': '',
            'vText5': '',
            'vText4': '',
            'vText3': '',
            'vText2': '',
            'icognoid': 'wsf',  # Never modified
            'icognocheck': '',
            'fno': 0,  # Never modified
            'prevref': '',
            'emotionaloutput': '',  # Never modified
            'emotionalhistory': '',  # Never modified
            'asbotname': '',  # Never modified
            'ttsvoice': '',  # Never modified
            'typing': '',  # Never modified
            'lineref': '',
            'sub': 'Say',  # Never modified
            'islearning': 1,  # Never modified
            'cleanslate': False,  # Never modified
        }

        # the log of our conversation with Cleverbot
        self.conversation = []
        self.resp = str()

    def ask(self, question):
        """Asks Cleverbot a question.
        
        Maintains message history.

        Args:
            q (str): The question to ask

        Returns:
            Cleverbot's answer
        """
        # Set the current question
        self.data['stimulus'] = question

        # Connect to Cleverbot's API and remember the response
        try:
            self.resp = self._send()
        except urllib2.HTTPError:
            # request failed. returning empty string
            return str()

        # Add the current question to the conversation log
        self.conversation.append(question)

        parsed = self._parse()

        # Set data as appropriate
        if self.data['sessionid'] != '':
            self.data['sessionid'] = parsed['conversation_id']

        # Add Cleverbot's reply to the conversation log
        self.conversation.append(parsed['answer'])

        return parsed['answer']

    def _send(self):
        """POST the user's question and all required information to the 
        Cleverbot API

        Cleverbot tries to prevent unauthorized access to its API by
        obfuscating how it generates the 'icognocheck' token, so we have
        to URLencode the data twice: once to generate the token, and
        twice to add the token to the data we're sending to Cleverbot.
        """
        # Set data as appropriate
        if self.conversation:
            linecount = 1
            for line in reversed(self.conversation):
                linecount += 1
                self.data['vText' + str(linecount)] = line
                if linecount == 8:
                    break

        # Generate the token
        enc_data = urllib.urlencode(self.data)
        digest_txt = enc_data[9:35]
        token = hashlib.md5(digest_txt).hexdigest()
        self.data['icognocheck'] = token

        # Add the token to the data
        enc_data = urllib.urlencode(self.data)
        req = urllib2.Request(self.API_URL, enc_data, self.headers)

        # POST the data to Cleverbot's API
        conn = urllib2.urlopen(req)
        resp = conn.read()

        # Return Cleverbot's response
        return resp

    def _parse(self):
        """Parses Cleverbot's response"""
        parsed = [
            item.split('\r') for item in self.resp.split('\r\r\r\r\r\r')[:-1]
        ]

        #print parsed

        '''
        [["Hmmm.. I don't know.", 'RSH00935295', 'j2log-vEaIElWHMXDBZAOAGQZE-detail', '', '', '', 'Hi. How are you?', "I'm awful.. You?", "Sincere question - I'm not trying to make a point. But do you ever worry about your carbon footprint? You fly an awful lot.", "Hmmm.. I don't know.", 'WA010150814'], ["Hmmm.. I don't know."]]

        [['I know little about you.', 'VWQ41375942', 'j2log-rWkOEuDUXLPLZACSOCOG-detail', '', 'Hi. How are you?', "I'm awful.. You?", "But do you ever worry about your carbon footprint?", 'How do know so much about swallows?', 'I know little about you.', '', '+3000_cbfull', '', '', '', '', 'I know that you are a proto-AI developed by the people who made Jabberwocky']]
        '''

        # I added this line because the second list was not being added sometimes
        #if len(parsed) > 2:
        #    parsed.append([parsed[0][-1]])

        return {
            'answer': parsed[0][0],
            'conversation_id': parsed[0][1],
            'conversation_log_id': parsed[0][2],
            'unknown': ""
            #'unknown': parsed[1][-1]
        }
