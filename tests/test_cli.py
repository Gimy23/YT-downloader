"""Integration and CLI tests using subprocess."""
import subprocess
import unittest

class TestCLI(unittest.TestCase):
    def test_version_command(self):
        res = subprocess.run(["ytdl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("1.0.0", res.stdout)

    def test_help_command(self):
        res = subprocess.run(["ytdl", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("download", res.stdout)
        self.assertIn("audio", res.stdout)

    def test_config_show(self):
        res = subprocess.run(["ytdl", "config", "--show", "--no-ui"], stdout=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("default_video_quality", res.stdout)

    def test_history_list(self):
        res = subprocess.run(["ytdl", "history", "--no-ui"], stdout=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0)

    def test_download_mock(self):
        res = subprocess.run(["ytdl", "download", "https://example.com/cli_test", "--no-ui"], stdout=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("SUCCESS", res.stdout)

if __name__ == "__main__":
    unittest.main()
