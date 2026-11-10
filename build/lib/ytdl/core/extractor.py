"""Metadata extraction."""
from __future__ import annotations
from typing import List
from ytdl.compat import ExtractorError, YoutubeDL
from ytdl.models.download import MediaFormat, VideoInfo

class MediaExtractor:
    def __init__(self, quiet: bool = True) -> None:
        self.opts = {
            "quiet": quiet,
            "no_warnings": True,
            "skip_download": True,
            "extractor_args": {"youtube": {"player_client": ["android", "web", "mweb"]}},
        }

    def extract(self, url: str) -> VideoInfo:
        with YoutubeDL(self.opts) as ydl:
            try:
                raw = ydl.extract_info(url, download=False)
            except Exception as exc:
                raise ExtractorError(f"Failed to inspect media: {exc}") from exc
        if not raw:
            raise ExtractorError("No media stream data found.")

        is_pl = "entries" in raw
        entries = list(raw.get("entries") or []) if is_pl else []
        formats: List[MediaFormat] = []
        for f in (raw.get("formats") or []):
            formats.append(
                MediaFormat(
                    format_id=str(f.get("format_id", "")),
                    ext=str(f.get("ext", "")),
                    resolution=str(f.get("resolution") or f.get("format_note") or "unknown"),
                    height=f.get("height"),
                    width=f.get("width"),
                    filesize=f.get("filesize") or f.get("filesize_approx"),
                    vcodec=f.get("vcodec"),
                    acodec=f.get("acodec"),
                )
            )

        return VideoInfo(
            id=str(raw.get("id", "")),
            title=str(raw.get("title", "Untitled Media")),
            uploader=str(raw.get("uploader") or raw.get("channel") or "Unknown Author"),
            duration=int(raw.get("duration") or 0),
            webpage_url=str(raw.get("webpage_url") or url),
            thumbnail=str(raw.get("thumbnail") or ""),
            formats=formats,
            is_playlist=is_pl,
            playlist_title=str(raw.get("title")) if is_pl else None,
            playlist_count=len(entries) if is_pl else None,
        )
