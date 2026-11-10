"""Format selector builders."""
from __future__ import annotations
from typing import Any, Dict, List

def build_video_format_string(quality: str, output_ext: str = "mp4") -> str:
    q = quality.lower().strip()
    if q == "best":
        return f"bestvideo[ext={output_ext}]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    if q.endswith("p"):
        try:
            h = int(q[:-1])
            return (
                f"bestvideo[height<={h}][ext={output_ext}]+bestaudio[ext=m4a]/"
                f"bestvideo[height<={h}]+bestaudio/"
                f"best[height<={h}]/best"
            )
        except ValueError:
            pass
    return "bestvideo+bestaudio/best"

def build_audio_postprocessors(fmt: str, quality: str = "192") -> List[Dict[str, Any]]:
    return [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": fmt.lower().strip(),
            "preferredquality": quality,
            "nopostoverwrites": False,
        }
    ]
