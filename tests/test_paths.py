"""Unit tests for path resolution and filename sanitization."""
import unittest
from pathlib import Path
from ytdl.utils.paths import (
    get_config_dir,
    get_data_dir,
    get_default_download_dir,
    resolve_output_path,
    sanitize_filename,
)

class TestPaths(unittest.TestCase):
    def test_default_download_dir(self):
        d = get_default_download_dir()
        self.assertIsInstance(d, Path)
        self.assertTrue("YT-Downloads" in str(d))

    def test_config_dir(self):
        d = get_config_dir()
        self.assertIsInstance(d, Path)
        self.assertTrue("ytdl" in str(d))

    def test_data_dir(self):
        d = get_data_dir()
        self.assertIsInstance(d, Path)
        self.assertTrue("ytdl" in str(d))

    def test_sanitize_filename(self):
        # Disallowed characters replaced with underscore
        self.assertEqual(sanitize_filename("test:video<1080p>?*.mp4"), "test_video_1080p_.mp4")
        self.assertEqual(sanitize_filename(""), "untitled_download")
        # Windows reserved words
        self.assertTrue(sanitize_filename("CON.mp4").startswith("_CON"))
        self.assertTrue(sanitize_filename("AUX.mp3").startswith("_AUX"))

    def test_resolve_output_path(self, tmp_path=None):
        out = resolve_output_path("/tmp/ytdl_test_custom_dir")
        self.assertTrue(out.exists())
        self.assertTrue(out.is_dir())

if __name__ == "__main__":
    unittest.main()
