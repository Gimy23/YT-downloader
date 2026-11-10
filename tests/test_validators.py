"""Unit tests for validators."""
import unittest
from ytdl.utils.validators import (
    is_valid_url,
    parse_playlist_range,
    validate_audio_format,
    validate_url,
    validate_video_quality,
)

class TestValidators(unittest.TestCase):
    def test_valid_urls(self):
        self.assertTrue(is_valid_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        self.assertTrue(is_valid_url("https://youtu.be/dQw4w9WgXcQ"))
        self.assertTrue(is_valid_url("http://example.com/video.mp4"))

    def test_invalid_urls(self):
        self.assertFalse(is_valid_url("not_a_url"))
        self.assertFalse(is_valid_url(""))
        self.assertFalse(is_valid_url("ftp://server/file"))
        with self.assertRaises(ValueError):
            validate_url("invalid_url")

    def test_validate_audio_format(self):
        self.assertEqual(validate_audio_format("mp3"), "mp3")
        self.assertEqual(validate_audio_format("FLAC"), "flac")
        self.assertEqual(validate_audio_format(".wav"), "wav")
        with self.assertRaises(ValueError):
            validate_audio_format("exe")

    def test_validate_video_quality(self):
        self.assertEqual(validate_video_quality("best"), "best")
        self.assertEqual(validate_video_quality("1080p"), "1080p")
        self.assertEqual(validate_video_quality("720P"), "720p")
        with self.assertRaises(ValueError):
            validate_video_quality("unknown_res")

    def test_parse_playlist_range(self):
        self.assertEqual(parse_playlist_range(None), (None, None))
        self.assertEqual(parse_playlist_range("1-5"), (1, 5))
        self.assertEqual(parse_playlist_range("3"), (3, 3))
        self.assertEqual(parse_playlist_range("2-"), (2, None))
        with self.assertRaises(ValueError):
            parse_playlist_range("5-2")
        with self.assertRaises(ValueError):
            parse_playlist_range("0")

if __name__ == "__main__":
    unittest.main()
