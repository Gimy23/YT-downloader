"""Unit tests for configuration persistence."""
import shutil
import tempfile
import unittest
from pathlib import Path
from ytdl.models.settings import AppConfig
from ytdl.services.config_service import ConfigService

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.service = ConfigService(config_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_default_config(self):
        cfg = self.service.load()
        self.assertIsInstance(cfg, AppConfig)
        self.assertEqual(cfg.default_video_quality, "best")
        self.assertEqual(cfg.default_audio_format, "mp3")

    def test_update_config(self):
        self.service.update(default_video_quality="1080p", default_audio_format="flac")
        cfg2 = self.service.load()
        self.assertEqual(cfg2.default_video_quality, "1080p")
        self.assertEqual(cfg2.default_audio_format, "flac")

    def test_reset_config(self):
        self.service.update(default_video_quality="720p")
        self.service.reset()
        cfg = self.service.load()
        self.assertEqual(cfg.default_video_quality, "best")

if __name__ == "__main__":
    unittest.main()
