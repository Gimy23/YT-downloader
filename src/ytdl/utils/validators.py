"""Input validation routines."""
from __future__ import annotations
import re
from typing import Optional, Tuple

SUPPORTED_AUDIO = {"mp3", "m4a", "wav", "flac", "opus"}
SUPPORTED_QUALITY = {"best", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"}
URL_REGEX = re.compile(r'^(https?://)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(/.*)?$', re.IGNORECASE)

def is_valid_url(url: str) -> bool:
    return bool(url and isinstance(url, str) and URL_REGEX.match(url.strip()))

def validate_url(url: str) -> str:
    cleaned = url.strip()
    if not is_valid_url(cleaned):
        raise ValueError(f"Invalid URL: '{url}'. Please enter a valid http:// or https:// address.")
    return cleaned

def validate_audio_format(fmt: str) -> str:
    normalized = fmt.strip().lower().lstrip(".")
    if normalized not in SUPPORTED_AUDIO:
        supported = ", ".join(sorted(SUPPORTED_AUDIO))
        raise ValueError(f"Unsupported audio format '{fmt}'. Supported: {supported}")
    return normalized

def validate_video_quality(quality: str) -> str:
    normalized = quality.strip().lower()
    if normalized not in SUPPORTED_QUALITY:
        supported = ", ".join(sorted(SUPPORTED_QUALITY, reverse=True))
        raise ValueError(f"Unsupported quality '{quality}'. Supported presets: {supported}")
    return normalized

def parse_playlist_range(range_str: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if not range_str:
        return (None, None)
    cleaned = range_str.strip()
    if "-" in cleaned:
        p1, p2 = cleaned.split("-", 1)
        s = int(p1.strip()) if p1.strip() else None
        e = int(p2.strip()) if p2.strip() else None
        if s is not None and s < 1:
            raise ValueError(f"Range start must be >= 1, got {s}")
        if e is not None and s is not None and e < s:
            raise ValueError(f"Range end ({e}) cannot be less than start ({s})")
        return (s, e)
    s_int = int(cleaned)
    if s_int < 1:
        raise ValueError(f"Range must be >= 1, got {s_int}")
    return (s_int, s_int)

import urllib.parse

def clean_media_url(url: str, is_playlist: bool = False) -> str:
    cleaned = url.strip()
    try:
        parsed = urllib.parse.urlparse(cleaned)
        if ("youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc) and not is_playlist:
            qs = urllib.parse.parse_qs(parsed.query)
            if "v" in qs:
                # Keep only video ID, strip radio/mix parameters and tracking tokens
                clean_qs = {"v": qs["v"][0]}
                return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', urllib.parse.urlencode(clean_qs), ''))
    except Exception:
        pass
    return cleaned


def normalize_playlist_url(url: str) -> str:
    cleaned = url.strip()
    try:
        parsed = urllib.parse.urlparse(cleaned)
        if "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:
            qs = urllib.parse.parse_qs(parsed.query)
            if "list" in qs:
                pl_id = qs["list"][0]
                return f"https://www.youtube.com/playlist?list={pl_id}"
    except Exception:
        pass
    return cleaned
