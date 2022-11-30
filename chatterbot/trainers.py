import os
import sys
import csv
import time
from dateutil import parser as date_parser
from chatterbot.conversation import Statement
from chatterbot.tagging import PosLemmaTagger
from chatterbot import utils


class Trainer(object):
    """
    Base class for all other trainer classes.

    :param boolean show_training_progress: Show progress indicators for the
           trainer. The environment variable ``CHATTERBOT_SHOW_TRAINING_PROGRESS``
           can also be set to control this. ``show_training_progress`` will override
           the environment variable if it is set.
    """

    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot

        environment_default = os.getenv('CHATTERBOT_SHOW_TRAINING_PROGRESS', True)
        self.show_training_progress = kwargs.get(
            'show_training_progress',
            environment_default
        )

    def get_preprocessed_statement(self, input_statement):
        """
        Preprocess the input statement.
        """
        for preprocessor in self.chatbot.preprocessors:
            input_statement = preprocessor(input_statement)

        return input_statement

    def train(self, *args, **kwargs):
        """
        This method must be overridden by a child class.
        """
        raise self.TrainerInitializationException()

    class TrainerInitializationException(Exception):
        """
        Exception raised when a base class has not overridden
        the required methods on the Trainer base class.
        """

        def __init__(self, message=None):
            default = (
                'A training class must be specified before calling train(). '
                'See http://chatterbot.readthedocs.io/en/stable/training.html'
            )
            super().__init__(message or default)

    def _generate_export_data(self):
        result = []
        for statement in self.chatbot.storage.filter():
            if statement.in_response_to:
                result.append([statement.in_response_to, statement.text])

        return result

    def export_for_training(self, file_path='./export.json'):
        """
        Create a file from the database that can be used to
        train other chat bots.
        """
        import json
        export = {'conversations': self._generate_export_data()}
        with open(file_path, 'w+', encoding='utf8') as jsonfile:
            json.dump(export, jsonfile, ensure_ascii=False)


class ListTrainer(Trainer):
    """
    Allows a chat bot to be trained using a list of strings
    where the list represents a conversation.
    """

    def train(self, conversation):
        """
        Train the chat bot based on the provided list of
        statements that represents a single conversation.
        """
        previous_statement_text = None
        previous_statement_search_text = ''

        statements_to_create = []

        for conversation_count, text in enumerate(conversation):
            if self.show_training_progress:
                utils.print_progress_bar(
                    'List Trainer',
                    conversation_count + 1, len(conversation)
                )

            statement_search_text = self.chatbot.storage.tagger.get_text_index_string(text)

            statement = self.get_preprocessed_statement(
                Statement(
                    text=text,
                    search_text=statement_search_text,
                    in_response_to=previous_statement_text,
                    search_in_response_to=previous_statement_search_text,
                    conversation='training'
                )
            )

            previous_statement_text = statement.text
            previous_statement_search_text = statement_search_text

            statements_to_create.append(statement)

        self.chatbot.storage.create_many(statements_to_create)


class ChatterBotCorpusTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    def train(self, *corpus_paths):
        from chatterbot.corpus import load_corpus, list_corpus_files

        data_file_paths = []

        # Get the paths to each file the bot will be trained with
        for corpus_path in corpus_paths:
            data_file_paths.extend(list_corpus_files(corpus_path))

        for corpus, categories, file_path in load_corpus(*data_file_paths):

            statements_to_create = []

            # Train the chat bot with each statement and response pair
            for conversation_count, conversation in enumerate(corpus):

                if self.show_training_progress:
                    utils.print_progress_bar(
                        'Training ' + str(os.path.basename(file_path)),
                        conversation_count + 1,
                        len(corpus)
                    )

                previous_statement_text = None
                previous_statement_search_text = ''

                for text in conversation:

                    statement_search_text = self.chatbot.storage.tagger.get_text_index_string(text)

                    statement = Statement(
                        text=text,
                        search_text=statement_search_text,
                        in_response_to=previous_statement_text,
                        search_in_response_to=previous_statement_search_text,
                        conversation='training'
                    )

                    statement.add_tags(*categories)

                    statement = self.get_preprocessed_statement(statement)

                    previous_statement_text = statement.text
                    previous_statement_search_text = statement_search_text

                    statements_to_create.append(statement)

            if statements_to_create:
                self.chatbot.storage.create_many(statements_to_create)


class UbuntuCorpusTrainer(Trainer):
    """
    Allow chatbots to be trained with the data from the Ubuntu Dialog Corpus.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        home_directory = os.path.expanduser('~')

        self.data_download_url = kwargs.get(
            'ubuntu_corpus_data_download_url',
            'http://cs.mcgill.ca/~jpineau/datasets/ubuntu-corpus-1.0/ubuntu_dialogs.tgz'
        )

        self.data_directory = kwargs.get(
            'ubuntu_corpus_data_directory',
            os.path.join(home_directory, 'ubuntu_data')
        )

        self.extracted_data_directory = os.path.join(
            self.data_directory, 'ubuntu_dialogs'
        )

        # Create the data directory if it does not already exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def is_downloaded(self, file_path):
        """
        Check if the data file is already downloaded.
        """
        if os.path.exists(file_path):
            self.chatbot.logger.info('File is already downloaded')
            return True

        return False

    def is_extracted(self, file_path):
        """
        Check if the data file is already extracted.
        """

        if os.path.isdir(file_path):
            self.chatbot.logger.info('File is already extracted')
            return True
        return False

    def download(self, url, show_status=True):
        """
        Download a file from the given url.
        Show a progress indicator for the download status.
        Based on: http://stackoverflow.com/a/15645088/1547223
        """
        import requests

        file_name = url.split('/')[-1]
        file_path = os.path.join(self.data_directory, file_name)

        # Do not download the data if it already exists
        if self.is_downloaded(file_path):
            return file_path

        with open(file_path, 'wb') as open_file:
            print('Downloading %s' % url)
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                # No content length header
                open_file.write(response.content)
            else:
                download = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    download += len(data)
                    open_file.write(data)
                    if show_status:
                        done = int(50 * download / total_length)
                        sys.stdout.write('\r[%s%s]' % ('=' * done, ' ' * (50 - done)))
                        sys.stdout.flush()

            # Add a new line after the download bar
            sys.stdout.write('\n')

        print('Download location: %s' % file_path)
        return file_path

    def extract(self, file_path):
        """
        Extract a tar file at the specified file path.
        """
        import tarfile

        print('Extracting {}'.format(file_path))

        if not os.path.exists(self.extracted_data_directory):
            os.makedirs(self.extracted_data_directory)

        def track_progress(members):
            sys.stdout.write('.')
            for member in members:
                # This will be the current file being extracted
                yield member

        with tarfile.open(file_path) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=self.extracted_data_directory, members=track_progress(tar))

        self.chatbot.logger.info('File extracted to {}'.format(self.extracted_data_directory))

        return True

    def train(self):
        import glob

        tagger = PosLemmaTagger(language=self.chatbot.storage.tagger.language)

        # Download and extract the Ubuntu dialog corpus if needed
        corpus_download_path = self.download(self.data_download_url)

        # Extract if the directory does not already exist
        if not self.is_extracted(self.extracted_data_directory):
            self.extract(corpus_download_path)

        extracted_corpus_path = os.path.join(
            self.extracted_data_directory,
            '**', '**', '*.tsv'
        )

        def chunks(items, items_per_chunk):
            for start_index in range(0, len(items), items_per_chunk):
                end_index = start_index + items_per_chunk
                yield items[start_index:end_index]

        file_list = glob.glob(extracted_corpus_path)

        file_groups = tuple(chunks(file_list, 10000))

        start_time = time.time()

        for tsv_files in file_groups:

            statements_from_file = []

            for tsv_file in tsv_files:
                with open(tsv_file, 'r', encoding='utf-8') as tsv:
                    reader = csv.reader(tsv, delimiter='\t')

                    previous_statement_text = None
                    previous_statement_search_text = ''

                    for row in reader:
                        if len(row) > 0:
                            statement = Statement(
                                text=row[3],
                                in_response_to=previous_statement_text,
                                conversation='training',
                                created_at=date_parser.parse(row[0]),
                                persona=row[1]
                            )

                            for preprocessor in self.chatbot.preprocessors:
                                statement = preprocessor(statement)

                            statement.search_text = tagger.get_text_index_string(statement.text)
                            statement.search_in_response_to = previous_statement_search_text

                            previous_statement_text = statement.text
                            previous_statement_search_text = statement.search_text

                            statements_from_file.append(statement)

            self.chatbot.storage.create_many(statements_from_file)

        print('Training took', time.time() - start_time, 'seconds.')
