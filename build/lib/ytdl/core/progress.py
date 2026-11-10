"""Progress dispatcher and yt-dlp callback hook."""
from __future__ import annotations
import time
from typing import Any, Callable, Dict, List, Optional
from ytdl.models.download import DownloadProgress

class ProgressDispatcher:
    def __init__(self) -> None:
        self._listeners: List[Callable[[DownloadProgress], None]] = []
        self._last_time: float = 0.0

    def add_listener(self, fn: Callable[[DownloadProgress], None]) -> None:
        if fn not in self._listeners:
            self._listeners.append(fn)

    def remove_listener(self, fn: Callable[[DownloadProgress], None]) -> None:
        if fn in self._listeners:
            self._listeners.remove(fn)

    def dispatch(self, p: DownloadProgress, force: bool = False) -> None:
        now = time.time()
        if force or (now - self._last_time >= 0.05) or p.status in ("finished", "error"):
            self._last_time = now
            for listener in self._listeners:
                try:
                    listener(p)
                except Exception:
                    pass

class YtdlpProgressHook:
    def __init__(self, dispatcher: ProgressDispatcher) -> None:
        self.dispatcher = dispatcher

    def __call__(self, d: Dict[str, Any]) -> None:
        st = d.get("status", "downloading")
        tot = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        dl = d.get("downloaded_bytes") or 0
        pct = (dl / tot * 100.0) if tot > 0 else 0.0
        prog = DownloadProgress(
            status=st,
            filename=d.get("filename", ""),
            total_bytes=tot,
            downloaded_bytes=dl,
            speed=d.get("speed") or 0.0,
            eta=d.get("eta"),
            percentage=min(100.0, pct),
        )
        self.dispatcher.dispatch(prog, force=(st in ("finished", "error")))
