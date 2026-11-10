"""Models for download streams and results."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

@dataclass
class MediaFormat:
    format_id: str
    ext: str
    resolution: str = "unknown"
    height: Optional[int] = None
    width: Optional[int] = None
    filesize: Optional[int] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    note: str = ""

@dataclass
class VideoInfo:
    id: str
    title: str
    uploader: str = "Unknown"
    duration: int = 0
    webpage_url: str = ""
    thumbnail: str = ""
    formats: List[MediaFormat] = field(default_factory=list)
    is_playlist: bool = False
    playlist_title: Optional[str] = None
    playlist_count: Optional[int] = None

    @property
    def formatted_duration(self) -> str:
        if not self.duration or self.duration <= 0:
            return "Live / Unknown"
        hours, rem = divmod(self.duration, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"

    @property
    def available_resolutions(self) -> List[str]:
        res_set = set()
        for f in self.formats:
            if f.height and f.height > 0:
                res_set.add(f"{f.height}p")
        return sorted(list(res_set), key=lambda x: int(x.rstrip("p")), reverse=True)

@dataclass
class DownloadProgress:
    status: str = "starting"
    filename: str = ""
    total_bytes: int = 0
    downloaded_bytes: int = 0
    speed: float = 0.0
    eta: Optional[int] = None
    percentage: float = 0.0

    @property
    def speed_human(self) -> str:
        return f"{self.speed / (1024 * 1024):.1f} MB/s" if self.speed > 0 else "-- MB/s"

    @property
    def eta_human(self) -> str:
        if self.eta is None or self.eta < 0:
            return "--:--"
        m, s = divmod(self.eta, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

    @property
    def downloaded_human(self) -> str:
        return f"{self.downloaded_bytes / (1024 * 1024):.1f} MB" if self.downloaded_bytes > 0 else "0 MB"

    @property
    def total_human(self) -> str:
        return f"{self.total_bytes / (1024 * 1024):.1f} MB" if self.total_bytes > 0 else "Unknown"

@dataclass
class DownloadResult:
    success: bool
    url: str
    title: str = ""
    filename: Optional[str] = None
    file_path: Optional[Path] = None
    file_size_bytes: int = 0
    duration_seconds: float = 0.0
    error_message: Optional[str] = None
    media_type: str = "video"
    quality_or_format: str = ""

    @property
    def file_size_human(self) -> str:
        return f"{self.file_size_bytes / (1024 * 1024):.2f} MB" if self.file_size_bytes > 0 else "Unknown"

@dataclass
class DownloadHistoryItem:
    id: str
    title: str
    url: str
    date: str
    filename: str
    output_path: str
    status: str
    media_type: str = "video"
    file_size_bytes: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "date": self.date,
            "filename": self.filename,
            "output_path": self.output_path,
            "status": self.status,
            "media_type": self.media_type,
            "file_size_bytes": self.file_size_bytes,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DownloadHistoryItem":
        return cls(
            id=d.get("id", ""),
            title=d.get("title", "Untitled"),
            url=d.get("url", ""),
            date=d.get("date", ""),
            filename=d.get("filename", ""),
            output_path=d.get("output_path", ""),
            status=d.get("status", "completed"),
            media_type=d.get("media_type", "video"),
            file_size_bytes=d.get("file_size_bytes", 0),
        )
