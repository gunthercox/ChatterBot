from unittest.mock import Mock
from io import BytesIO
import tarfile
import os
import requests
from tests.base_case import ChatBotTestCase
from chatterbot.trainers import UbuntuCorpusTrainer


class UbuntuCorpusTrainerTestCase(ChatBotTestCase):
    """
    Test the Ubuntu Corpus trainer class.
    """

    def setUp(self):
        super().setUp()
        self.trainer = UbuntuCorpusTrainer(
            self.chatbot,
            ubuntu_corpus_data_directory='./.ubuntu_test_data/',
            show_training_progress=False
        )

        # Fake download url
        self.data_download_url = 'https://docs.chatterbot.us/ubuntu_dialogs.tgz'

    def tearDown(self):
        super().tearDown()

        self._remove_data()

    def _get_data(self):

        data1 = (
            b'2004-11-04T16:49:00.000Z	tom	jane	Hello\n'
            b'2004-11-04T16:49:00.000Z	tom	jane	Is anyone there?\n'
            b'2004-11-04T16:49:00.000Z	jane		Yes\n'
            b'\n'
        )

        data2 = (
            b'2004-11-04T16:49:00.000Z	tom	jane	Hello\n'
            b'2004-11-04T16:49:00.000Z	tom		Is anyone there?\n'
            b'2004-11-04T16:49:00.000Z	jane		Yes\n'
            b'\n'
        )

        return data1, data2

    def _remove_data(self):
        """
        Clean up by removing the corpus data directory.
        """
        import shutil

        if os.path.exists(self.trainer.data_directory):
            shutil.rmtree(self.trainer.data_directory)

    def _create_test_corpus(self, data):
        """
        Create a small tar in a similar format to the
        Ubuntu corpus file in memory for testing.
        """
        file_path = os.path.join(self.trainer.data_directory, 'ubuntu_dialogs.tgz')
        os.makedirs(self.trainer.data_directory, exist_ok=True)
        tar = tarfile.TarFile(file_path, 'a')

        tsv1 = BytesIO(data[0])
        tsv2 = BytesIO(data[1])

        tarinfo = tarfile.TarInfo('dialogs/3/1.tsv')
        tarinfo.size = len(data[0])
        tar.addfile(tarinfo, fileobj=tsv1)

        tarinfo = tarfile.TarInfo('dialogs/3/2.tsv')
        tarinfo.size = len(data[1])
        tar.addfile(tarinfo, fileobj=tsv2)

        tsv1.close()
        tsv2.close()
        tar.close()

        return file_path

    def _destroy_test_corpus(self):
        """
        Remove the test corpus file.
        """
        file_path = os.path.join(self.trainer.data_directory, 'ubuntu_dialogs.tgz')

        if os.path.exists(file_path):
            os.remove(file_path)

    def _mock_get_response(self, *args, **kwargs):
        """
        Return a requests.Response object.
        """
        response = requests.Response()
        response._content = b'Some response content'
        response.headers['content-length'] = len(response.content)
        return response

    def test_download(self):
        """
        Test the download function for the Ubuntu corpus trainer.
        """
        requests.get = Mock(side_effect=self._mock_get_response)
        download_url = 'https://example.com/download.tgz'
        self.trainer.download(download_url, show_status=False)

        file_name = download_url.split('/')[-1]
        downloaded_file_path = os.path.join(self.trainer.data_directory, file_name)

        requests.get.assert_called_with(download_url, stream=True)
        self.assertTrue(os.path.exists(downloaded_file_path))

        # Remove the dummy download_url
        os.remove(downloaded_file_path)

    def test_download_file_exists(self):
        """
        Test the case that the corpus file exists.
        """
        file_path = os.path.join(self.trainer.data_directory, 'download.tgz')
        os.makedirs(self.trainer.data_directory, exist_ok=True)
        open(file_path, 'a').close()

        requests.get = Mock(side_effect=self._mock_get_response)
        download_url = 'https://example.com/download.tgz'
        self.trainer.download(download_url, show_status=False)

        # Remove the dummy download_url
        os.remove(file_path)

        self.assertFalse(requests.get.called)

    def test_download_url_not_found(self):
        """
        Test the case that the url being downloaded does not exist.
        """
        self.skipTest('This test needs to be created.')

    def test_extract(self):
        """
        Test the extraction of text from a decompressed Ubuntu Corpus file.
        """
        file_object_path = self._create_test_corpus(self._get_data())
        self.trainer.extract(file_object_path)

        self._destroy_test_corpus()
        corpus_path = os.path.join(self.trainer.data_path, 'dialogs', '3')

        self.assertTrue(os.path.exists(self.trainer.data_path))
        self.assertTrue(os.path.exists(os.path.join(corpus_path, '1.tsv')))
        self.assertTrue(os.path.exists(os.path.join(corpus_path, '2.tsv')))

    def test_train(self):
        """
        Test that the chat bot is trained using data from the Ubuntu Corpus.
        """
        self._create_test_corpus(self._get_data())

        self.trainer.train(self.data_download_url, limit=50)
        self._destroy_test_corpus()

        response = self.chatbot.get_response('Is anyone there?')
        self.assertEqual(response.text, 'Yes')

    def test_train_sets_search_text(self):
        """
        Test that the chat bot is trained using data from the Ubuntu Corpus.
        """
        self._create_test_corpus(self._get_data())

        self.trainer.train(self.data_download_url, limit=50)
        self._destroy_test_corpus()

        results = list(self.chatbot.storage.filter(text='Is anyone there?'))

        self.assertEqual(len(results), 2, msg='Results: {}'.format(results))
        self.assertEqual(results[0].search_text, 'AUX:anyone PRON:there')

    def test_train_sets_search_in_response_to(self):
        """
        Test that the chat bot is trained using data from the Ubuntu Corpus.
        """
        self._create_test_corpus(self._get_data())

        self.trainer.train(self.data_download_url, limit=50)
        self._destroy_test_corpus()

        results = list(self.chatbot.storage.filter(in_response_to='Is anyone there?'))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_in_response_to, 'AUX:anyone PRON:there')

    def test_is_extracted(self):
        """
        Test that a check can be done for if the corpus has aleady been extracted.
        """
        file_object_path = self._create_test_corpus(self._get_data())
        self.trainer.extract(file_object_path)

        extracted = self.trainer.is_extracted(self.trainer.data_path)
        self._destroy_test_corpus()

        self.assertTrue(extracted)

    def test_is_not_extracted(self):
        """
        Test that a check can be done for if the corpus has aleady been extracted.
        """
        self._remove_data()
        extracted = self.trainer.is_extracted(self.trainer.data_path)

        self.assertFalse(extracted)

    def test_extract_raises_on_symlink_data_path(self):
        """
        Test that extract() raises an exception when data_path is a symlink.

        A local attacker could pre-plant a symlink at the predictable
        data_path location to redirect archive extraction to an arbitrary
        directory. The trainer must reject a symlink target before extracting.
        """
        import tempfile
        import shutil

        attacker_target = tempfile.mkdtemp(prefix='cb_symlink_attack_')
        try:
            file_object_path = self._create_test_corpus(self._get_data())

            # Plant the symlink at data_path before extraction
            os.makedirs(self.trainer.data_directory, exist_ok=True)
            os.symlink(attacker_target, self.trainer.data_path)

            with self.assertRaises(Exception):
                self.trainer.extract(file_object_path)

            # Confirm nothing was written to the attacker's target directory
            self.assertEqual(
                os.listdir(attacker_target), [],
                'Files were written through the symlink to the attacker target directory'
            )
        finally:
            if os.path.islink(self.trainer.data_path):
                os.unlink(self.trainer.data_path)
            shutil.rmtree(attacker_target, ignore_errors=True)
            self._destroy_test_corpus()

    def test_extract_does_not_follow_symlink_members(self):
        """
        Test that safe_extract() rejects tar members whose resolved paths
        escape the extraction directory via a symlink.

        Even if data_path itself is legitimate, a tar archive containing a
        symlink member pointing outside the extraction root must be rejected.
        """
        import tempfile
        import shutil

        attacker_target = tempfile.mkdtemp(prefix='cb_member_symlink_attack_')
        try:
            os.makedirs(self.trainer.data_path, exist_ok=True)

            # Build a tar containing a directory entry that is a symlink
            # pointing outside the extraction root, plus a file routed through it.
            file_path = os.path.join(self.trainer.data_directory, 'malicious.tgz')
            with tarfile.TarFile(file_path, 'w') as tf:
                link_info = tarfile.TarInfo('escape_link')
                link_info.type = tarfile.SYMTYPE
                link_info.linkname = attacker_target
                tf.addfile(link_info)

                payload = b'should not be written outside extraction root\n'
                file_info = tarfile.TarInfo('escape_link/pwned.txt')
                file_info.size = len(payload)
                tf.addfile(file_info, BytesIO(payload))

            with self.assertRaises(Exception):
                self.trainer.extract(file_path)

            self.assertEqual(
                os.listdir(attacker_target), [],
                'Files were written outside the extraction root via a symlink member'
            )
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            shutil.rmtree(attacker_target, ignore_errors=True)

    def test_extract_raises_on_symlinked_data_directory(self):
        """
        Test that extract() raises when the parent data_directory (not just
        data_path) is a symlink.

        A local attacker can pre-create data_directory as a symlink before
        data_path exists beneath it. data_path itself will be a real
        directory once created, so checking only data_path is insufficient.
        """
        import tempfile
        import shutil

        attacker_target = tempfile.mkdtemp(prefix='cb_parent_symlink_attack_')
        try:
            file_object_path = self._create_test_corpus(self._get_data())

            # Replace data_directory itself with a symlink before extraction
            data_directory = os.path.normpath(self.trainer.data_directory)
            shutil.rmtree(data_directory, ignore_errors=True)
            os.symlink(attacker_target, data_directory)

            with self.assertRaises(Exception):
                self.trainer.extract(file_object_path)

            self.assertEqual(
                os.listdir(attacker_target), [],
                'Files were written through the symlinked parent directory'
            )
        finally:
            if os.path.islink(data_directory):
                os.unlink(data_directory)
            shutil.rmtree(attacker_target, ignore_errors=True)

    def test_extract_rejects_sibling_path_with_shared_prefix(self):
        """
        Test that a tar member whose path resolves to a sibling directory
        sharing a string prefix with data_path is rejected (e.g. data_path
        is '.../ubuntu_dialogs' and the member escapes into
        '.../ubuntu_dialogsEVIL').

        os.path.commonprefix() performs a character-by-character string
        comparison, not a path-component comparison, so '.../ubuntu_dialogs'
        is treated as a prefix of '.../ubuntu_dialogsEVIL' and the escape is
        incorrectly accepted. os.path.commonpath() must be used instead.
        """
        import shutil

        os.makedirs(self.trainer.data_path, exist_ok=True)
        sibling_dir = self.trainer.data_path.rstrip(os.sep) + 'EVIL'

        try:
            file_path = os.path.join(self.trainer.data_directory, 'sibling_escape.tgz')
            with tarfile.TarFile(file_path, 'w') as tf:
                payload = b'should not be written into the sibling directory\n'
                # Escapes the extraction root into a sibling dir that shares
                # a string prefix but is not actually contained within it.
                member_name = os.path.join('..', os.path.basename(sibling_dir), 'pwned.txt')
                member_info = tarfile.TarInfo(member_name)
                member_info.size = len(payload)
                tf.addfile(member_info, BytesIO(payload))

            with self.assertRaises(Exception):
                self.trainer.extract(file_path)

            self.assertFalse(
                os.path.exists(os.path.join(sibling_dir, 'pwned.txt')),
                'File was written into a sibling directory sharing a string prefix with data_path'
            )
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            shutil.rmtree(sibling_dir, ignore_errors=True)

    def test_extract_fails_closed_if_data_path_swapped_immediately_before_commit(self):
        """
        Test that extract() fails closed if data_path is replaced with a
        symlink in the instant between the pre-commit check and the final
        os.rename() call.

        extractall() writes archive members one at a time, so a single
        upfront symlink check on data_path leaves a window open for the
        remainder of the extraction. This test simulates an attacker who
        wins that race and plants the symlink immediately before the commit
        step, confirming that os.rename() itself fails closed (a directory
        cannot be renamed onto an existing symlink) instead of silently
        extracting through it.
        """
        import tempfile
        import shutil
        from unittest.mock import patch

        attacker_target = tempfile.mkdtemp(prefix='cb_toctou_rename_attack_')
        real_rename = os.rename

        def rename_after_attacker_swap(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            # dst may be a bare name resolved via dst_dir_fd (hardened path)
            # or a full path (fallback path); resolve to an absolute target
            # either way so the attacker's symlink lands in the right place.
            target_path = os.path.join(self.trainer.data_directory, dst) if dst_dir_fd is not None else dst
            # Simulate the attacker winning the race right before the commit.
            if not os.path.exists(target_path):
                os.symlink(attacker_target, target_path)
            return real_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

        try:
            file_object_path = self._create_test_corpus(self._get_data())

            with patch('chatterbot.trainers.os.rename', side_effect=rename_after_attacker_swap):
                with self.assertRaises(Exception):
                    self.trainer.extract(file_object_path)

            self.assertEqual(
                os.listdir(attacker_target), [],
                'Files were written through a symlink planted immediately before the atomic rename'
            )
        finally:
            if os.path.islink(self.trainer.data_path):
                os.unlink(self.trainer.data_path)
            shutil.rmtree(attacker_target, ignore_errors=True)
            self._destroy_test_corpus()

    def test_extract_stays_within_original_directory_when_data_directory_relocated(self):
        """
        Test that extraction never leaks into an attacker's directory if
        data_directory is renamed away and replaced with a symlink in the
        window between opening the verified directory fd and creating the
        staging directory.

        Anchoring only the mkdir/rename calls to the fd (via dir_fd) is not
        sufficient on its own: tarfile.extractall() writes through plain
        path strings and will silently recreate a missing destination
        through a freshly-planted symlink. The archive writes must also be
        anchored, via the /proc/self/fd/N magic path, so the extraction
        itself stays bound to the directory verified before the swap. The
        pre-commit symlink re-check then detects the swapped data_directory
        and aborts the commit, discarding the safely-extracted staging data
        rather than landing it somewhere the trainer can no longer find.

        Only meaningful on platforms with this hardening (Linux); skipped
        elsewhere, where the narrower pre-existing protections still apply.
        """
        from chatterbot.trainers import _DIR_FD_EXTRACTION_SUPPORTED

        if not _DIR_FD_EXTRACTION_SUPPORTED:
            self.skipTest('dir_fd + /proc/self/fd extraction hardening is not supported on this platform')

        import tempfile
        import shutil
        from unittest.mock import patch

        # Build the input archive in an independent location so that
        # relocating data_directory mid-extraction doesn't also hide the
        # archive being read.
        independent_dir = tempfile.mkdtemp(prefix='cb_relocate_input_')
        data = self._get_data()
        file_object_path = os.path.join(independent_dir, 'corpus.tgz')
        with tarfile.TarFile(file_object_path, 'w') as tf:
            payload = data[0]
            info = tarfile.TarInfo('dialogs/3/1.tsv')
            info.size = len(payload)
            tf.addfile(info, BytesIO(payload))

        attacker_target = tempfile.mkdtemp(prefix='cb_relocate_attack_')
        data_directory = os.path.normpath(self.trainer.data_directory)
        relocated_original = data_directory + '.orig'
        real_mkdir = os.mkdir
        swapped = []

        def mkdir_after_relocation(*args, **kwargs):
            if not swapped:
                swapped.append(True)
                os.rename(data_directory, relocated_original)
                os.symlink(attacker_target, data_directory)
            return real_mkdir(*args, **kwargs)

        os.makedirs(data_directory, exist_ok=True)

        try:
            with patch('chatterbot.trainers.os.mkdir', side_effect=mkdir_after_relocation):
                # The pre-commit re-check detects the swapped data_directory
                # and aborts; the key property under test is that nothing
                # leaks to the attacker, not that this specific call succeeds.
                with self.assertRaises(Exception):
                    self.trainer.extract(file_object_path)

            self.assertEqual(
                os.listdir(attacker_target), [],
                'Files were written into the attacker directory after data_directory was relocated'
            )
        finally:
            if os.path.islink(data_directory):
                os.unlink(data_directory)
            shutil.rmtree(relocated_original, ignore_errors=True)
            shutil.rmtree(attacker_target, ignore_errors=True)
            shutil.rmtree(independent_dir, ignore_errors=True)

    def test_dir_fd_extraction_support_implies_procfs(self):
        """
        The dir_fd extraction path anchors tarfile's writes through
        /proc/self/fd/N, so it must stay disabled anywhere procfs is absent.
        Enabling it without procfs makes extract() fail on the first write.
        """
        from chatterbot import trainers

        if trainers._DIR_FD_EXTRACTION_SUPPORTED:
            self.assertTrue(
                os.path.isdir('/proc/self/fd'),
                'dir_fd extraction is enabled but /proc/self/fd is unavailable, '
                'so the extraction root resolves to a nonexistent path'
            )

    def test_download_refuses_symlinked_archive_path(self):
        """
        Test that train() refuses to write the corpus archive through a
        symlink planted at the archive path inside data_directory.

        is_downloaded() is a bare os.path.exists(), so a dangling symlink at
        the predictable archive path reads as not-yet-downloaded, and a plain
        open() would then create the link target rather than a file inside
        the data directory.
        """
        import tempfile
        import shutil

        attacker_directory = tempfile.mkdtemp(prefix='cb_download_symlink_attack_')
        attacker_target = os.path.join(attacker_directory, 'planted.tgz')
        archive_path = os.path.join(self.trainer.data_directory, 'ubuntu_dialogs.tgz')

        try:
            requests.get = Mock(side_effect=self._mock_get_response)

            os.makedirs(self.trainer.data_directory, exist_ok=True)
            os.symlink(attacker_target, archive_path)

            with self.assertRaises(self.trainer.TrainerInitializationException):
                self.trainer.train(self.data_download_url, limit=50)

            self.assertFalse(
                os.path.exists(attacker_target),
                'The archive was written through the symlink at the archive path'
            )
        finally:
            if os.path.islink(archive_path):
                os.unlink(archive_path)
            shutil.rmtree(attacker_directory, ignore_errors=True)
