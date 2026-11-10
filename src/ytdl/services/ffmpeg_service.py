"""FFmpeg detection service."""
from __future__ import annotations
import os
import shutil
import subprocess
from typing import Any, Dict, Optional

class FFmpegService:
    def __init__(self) -> None:
        self._path = shutil.which("ffmpeg")

    @property
    def is_available(self) -> bool:
        return bool(self._path and os.path.isfile(self._path))

    @property
    def ffmpeg_path(self) -> Optional[str]:
        return self._path

    def get_version(self) -> str:
        if not self.is_available:
            return "Not Installed"
        try:
            res = subprocess.run([self._path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3)
            first = res.stdout.splitlines()[0] if res.stdout else "Available"
            parts = first.split()
            if len(parts) >= 3 and parts[0] == "ffmpeg" and parts[1] == "version":
                return parts[2]
            return first[:25]
        except Exception:
            return "Available"

    def get_status(self) -> Dict[str, Any]:
        return {
            "available": self.is_available,
            "path": self._path or "Not found",
            "version": self.get_version(),
        }
