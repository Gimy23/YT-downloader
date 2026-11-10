"""Configuration models."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

@dataclass
class AppConfig:
    default_directory: Optional[str] = None
    default_video_quality: str = "best"
    default_audio_format: str = "mp3"
    preferred_output_format: str = "mp4"
    theme: str = "default"
    concurrent_downloads: int = 1
    filename_template: str = "%(title)s.%(ext)s"
    no_color: bool = False
    cookies_from_browser: Optional[str] = None
    cookies_file: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        valid = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid)
