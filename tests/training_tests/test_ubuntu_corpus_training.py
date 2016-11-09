from io import BytesIO
import tarfile
import os
from mock import Mock

from tests.base_case import ChatBotTestCase
from chatterbot.trainers import UbuntuCorpusTrainer


class UbuntuCorpusTrainerTestCase(ChatBotTestCase):
    """
    Test the Ubuntu Corpus trainer class.
    """

    def setUp(self):
        super(UbuntuCorpusTrainerTestCase, self).setUp()
        self.chatbot.set_trainer(UbuntuCorpusTrainer)

    def _create_test_corpus(self):
        """
        Create a small tar in a similar format to the
        Ubuntu corpus file in memory for testing.
        """
        tar = tarfile.TarFile('ubuntu_corpus.tar', 'w')

        data1 = (
            b'2004-11-04T16:49:00.000Z	tom		jane : Hello\n' +
            b'2004-11-04T16:49:00.000Z	tom		jane : Is anyone there?\n' +
            b'2004-11-04T16:49:00.000Z	jane	tom	I am good' +
            b'\n'
        )

        data2 = (
            b'2004-11-04T16:49:00.000Z	tom		jane : Hello\n' +
            b'2004-11-04T16:49:00.000Z	tom		jane : Is anyone there?\n' +
            b'2004-11-04T16:49:00.000Z	jane	tom	I am good' +
            b'\n'
        )

        tsv1 = BytesIO(data1)
        tsv2 = BytesIO(data2)

        tarinfo = tarfile.TarInfo('ubuntu_dialogs/3/1.tsv')
        tarinfo.size = len(data1)
        tar.addfile(tarinfo, fileobj=tsv1)

        tarinfo = tarfile.TarInfo('ubuntu_dialogs/3/2.tsv')
        tarinfo.size = len(data2)
        tar.addfile(tarinfo, fileobj=tsv2)

        tsv1.close()
        tsv2.close()
        tar.close()

        return os.path.realpath(tar.name)

    def test_download(self):
        """
        Test the download function for the Ubuntu corpus trainer.
        """
        import requests

        def mock_get_response(*args, **kwargs):
            response = requests.Response()
            response._content = b'Some response content'
            response.headers['content-length'] = len(response.content)
            return response

        requests.get = Mock(side_effect=mock_get_response)
        download_url = 'https://example.com/download.tar'
        # self.chatbot.trainer.requests.get = Mock()
        self.chatbot.trainer.download(download_url, show_status=False)
        requests.get.assert_called_with(download_url, stream=True)

    def test_download_does_not_exist(self):
        """
        Test the case that the file being downloaded does not exist.
        """
        pass

    def test_extract(self):
        """
        Test the extraction of text from a decompressed Ubuntu Corpus file.
        """
        file_object_path = self._create_test_corpus()
        self.chatbot.trainer.extract(file_object_path)

    def test_train(self):
        """
        Test that the chat bot is trained using data from the Ubuntu Corpus.
        """
        pass
