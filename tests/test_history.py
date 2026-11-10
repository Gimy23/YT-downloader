"""Unit tests for download history management."""
import shutil
import tempfile
import unittest
from pathlib import Path
from ytdl.services.history_service import HistoryService

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.service = HistoryService(data_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_history(self):
        items = self.service.get_all()
        self.assertEqual(items, [])

    def test_add_and_retrieve_history(self):
        item = self.service.add(
            title="Test Video",
            url="https://example.com/test",
            filename="test.mp4",
            output_path="/tmp/test.mp4",
            status="completed",
            media_type="video",
            file_size_bytes=1048576,
        )
        self.assertEqual(item.title, "Test Video")
        items = self.service.get_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].filename, "test.mp4")

    def test_clear_history(self):
        self.service.add(title="Item 1", url="http://a", filename="1.mp4", output_path="/tmp/1")
        self.service.add(title="Item 2", url="http://b", filename="2.mp4", output_path="/tmp/2")
        self.assertEqual(len(self.service.get_all()), 2)
        self.service.clear()
        self.assertEqual(len(self.service.get_all()), 0)

if __name__ == "__main__":
    unittest.main()
