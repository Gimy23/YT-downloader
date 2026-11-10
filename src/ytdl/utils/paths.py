"""Cross-platform path resolution and file sanitization."""
from __future__ import annotations
import os
import platform
import re
from pathlib import Path
from typing import Optional, Union

WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
}
ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

def is_windows() -> bool:
    return platform.system() == "Windows"

def get_default_download_dir() -> Path:
    home = Path.home()
    if is_windows():
        profile = os.environ.get("USERPROFILE")
        base = Path(profile) if profile else home
        return base / "Videos" / "YT-Downloads"
    return home / "Videos" / "YT-Downloads"

def get_config_dir() -> Path:
    home = Path.home()
    if is_windows():
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else (home / "AppData" / "Roaming")
        return base / "ytdl"
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else (home / ".config")
    return base / "ytdl"

def get_data_dir() -> Path:
    home = Path.home()
    if is_windows():
        local = os.environ.get("LOCALAPPDATA")
        base = Path(local) if local else (home / "AppData" / "Local")
        return base / "ytdl"
    xdg = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg) if xdg else (home / ".local" / "share")
    return base / "ytdl"

def resolve_output_path(output_dir: Optional[Union[str, Path]] = None) -> Path:
    if not output_dir:
        target = get_default_download_dir()
    else:
        target = Path(os.path.expandvars(os.path.expanduser(str(output_dir)))).resolve()
    target.mkdir(parents=True, exist_ok=True)
    return target

def sanitize_filename(filename: str, max_length: int = 200) -> str:
    if not filename:
        return "untitled_download"
    cleaned = ILLEGAL_CHARS.sub("_", filename).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.rstrip(". ")
    if not cleaned:
        cleaned = "untitled_download"
    root = cleaned.split(".")[0].upper()
    if root in WINDOWS_RESERVED:
        cleaned = f"_{cleaned}"
    if len(cleaned.encode("utf-8")) > max_length:
        parts = cleaned.rsplit(".", 1)
        ext = f".{parts[1]}" if len(parts) > 1 else ""
        allowed = max(10, max_length - len(ext))
        cleaned = parts[0][:allowed].rstrip(". ") + ext
    return cleaned
