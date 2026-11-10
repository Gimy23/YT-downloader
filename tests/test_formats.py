"""Unit tests for format string generation."""
import unittest
from ytdl.core.formats import build_audio_postprocessors, build_video_format_string

class TestFormats(unittest.TestCase):
    def test_best_quality_format(self):
        fmt = build_video_format_string("best", output_ext="mp4")
        self.assertTrue("bestvideo" in fmt)
        self.assertTrue("bestaudio" in fmt)

    def test_resolution_quality_format(self):
        fmt = build_video_format_string("1080p", output_ext="mp4")
        self.assertTrue("height<=1080" in fmt)

        fmt720 = build_video_format_string("720p")
        self.assertTrue("height<=720" in fmt720)

    def test_audio_postprocessors(self):
        pp = build_audio_postprocessors("mp3", quality="256")
        self.assertEqual(len(pp), 1)
        self.assertEqual(pp[0]["key"], "FFmpegExtractAudio")
        self.assertEqual(pp[0]["preferredcodec"], "mp3")
        self.assertEqual(pp[0]["preferredquality"], "256")

if __name__ == "__main__":
    unittest.main()
