"""History persistence service."""
from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from ytdl.models.download import DownloadHistoryItem
from ytdl.utils.paths import get_data_dir

class HistoryService:
    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self.data_dir = data_dir or get_data_dir()
        self.history_file = self.data_dir / "history.json"

    def get_all(self) -> List[DownloadHistoryItem]:
        if not self.history_file.exists():
            return []
        try:
            records = json.loads(self.history_file.read_text(encoding="utf-8"))
            return [DownloadHistoryItem.from_dict(r) for r in records]
        except Exception:
            return []

    def add(self, title: str, url: str, filename: str, output_path: str, status: str = "completed", media_type: str = "video", file_size_bytes: int = 0) -> DownloadHistoryItem:
        items = self.get_all()
        now_str = datetime.now(timezone.utc).isoformat()
        item = DownloadHistoryItem(
            id=str(uuid.uuid4())[:8],
            title=title,
            url=url,
            date=now_str,
            filename=filename,
            output_path=output_path,
            status=status,
            media_type=media_type,
            file_size_bytes=file_size_bytes,
        )
        items.insert(0, item)
        self._save(items)
        return item

    def clear(self) -> None:
        self._save([])

    def _save(self, items: List[DownloadHistoryItem]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        raw = [i.to_dict() for i in items[:500]]
        self.history_file.write_text(json.dumps(raw, indent=2), encoding="utf-8")
