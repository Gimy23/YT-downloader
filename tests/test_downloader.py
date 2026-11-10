"""Unit tests for Downloader and progress dispatching."""
import tempfile
import unittest
from ytdl.core.downloader import Downloader
from ytdl.core.progress import ProgressDispatcher
from ytdl.models.download import DownloadProgress

class TestDownloader(unittest.TestCase):
    def test_progress_dispatch(self):
        received = []
        dispatcher = ProgressDispatcher()
        dispatcher.add_listener(lambda p: received.append(p))

        p = DownloadProgress(status="downloading", percentage=50.0, speed=1048576, total_bytes=10000000)
        dispatcher.dispatch(p, force=True)

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].percentage, 50.0)
        self.assertEqual(received[0].speed_human, "1.0 MB/s")

    def test_mock_video_download(self):
        downloader = Downloader()
        with tempfile.TemporaryDirectory() as tmp_dir:
            res = downloader.download_video("https://example.com/test_video", quality="720p", output_dir=tmp_dir)
            self.assertTrue(res.success)
            self.assertEqual(res.quality_or_format, "720p")
            self.assertEqual(res.media_type, "video")

    def test_mock_audio_download(self):
        downloader = Downloader()
        with tempfile.TemporaryDirectory() as tmp_dir:
            res = downloader.download_audio("https://example.com/test_audio", audio_format="mp3", output_dir=tmp_dir)
            self.assertTrue(res.success)
            self.assertEqual(res.quality_or_format, "mp3")
            self.assertEqual(res.media_type, "audio")

    def test_mock_playlist_folder_creation(self):
        downloader = Downloader()
        with tempfile.TemporaryDirectory() as tmp_dir:
            results = downloader.download_playlist("https://example.com/playlist", quality="720p", output_dir=tmp_dir)
            self.assertTrue(len(results) >= 1)
            # Check that files were placed in a subfolder or output_dir
            for r in results:
                if r.file_path:
                    self.assertTrue(r.file_path.parent.exists())

if __name__ == "__main__":
    unittest.main()
