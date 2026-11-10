"""Core downloader engine."""
from __future__ import annotations
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
from ytdl.compat import YoutubeDL
from ytdl.core.formats import build_audio_postprocessors, build_video_format_string
from ytdl.core.progress import ProgressDispatcher, YtdlpProgressHook
from ytdl.models.download import DownloadProgress, DownloadResult
from ytdl.services.ffmpeg_service import FFmpegService
from ytdl.utils.paths import resolve_output_path
from ytdl.utils.validators import clean_media_url, normalize_playlist_url

class Downloader:
    def __init__(self, progress_dispatcher: Optional[ProgressDispatcher] = None, ffmpeg_service: Optional[FFmpegService] = None) -> None:
        self.dispatcher = progress_dispatcher or ProgressDispatcher()
        self.ffmpeg = ffmpeg_service or FFmpegService()

    def download_video(
        self,
        url: str,
        quality: str = "best",
        output_dir: Optional[Union[str, Path]] = None,
        preferred_format: str = "mp4",
        cookies_from_browser: Optional[str] = None,
        cookies_file: Optional[str] = None,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> DownloadResult:
        start = time.time()
        target = resolve_output_path(output_dir)
        clean_url = clean_media_url(url, is_playlist=False)

        if progress_callback:
            self.dispatcher.add_listener(progress_callback)

        hook = YtdlpProgressHook(self.dispatcher)
        fmt_str = build_video_format_string(quality, output_ext=preferred_format)
        outtmpl = str(target / "%(title)s.%(ext)s")

        opts: Dict[str, Any] = {
            "format": fmt_str,
            "outtmpl": outtmpl,
            "progress_hooks": [hook],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "continuedl": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web", "mweb"],
                    "player_skip": ["configs", "webpage"],
                }
            },
        }
        if cookies_from_browser:
            opts["cookiesfrombrowser"] = (cookies_from_browser,)
        elif cookies_file:
            opts["cookiefile"] = cookies_file

        if self.ffmpeg.is_available:
            opts["merge_output_format"] = preferred_format
            opts["ffmpeg_location"] = self.ffmpeg.ffmpeg_path

        title = "Unknown"
        final_fn = ""
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                if info:
                    title = info.get("title", "Unknown")
                    fn = ydl.prepare_filename(info)
                    if self.ffmpeg.is_available and preferred_format:
                        base, _ = os.path.splitext(fn)
                        merged = f"{base}.{preferred_format}"
                        final_fn = merged if os.path.isfile(merged) else fn
                    else:
                        final_fn = fn

            fpath = Path(final_fn) if final_fn and os.path.isfile(final_fn) else None
            size = fpath.stat().st_size if fpath and fpath.exists() else 0

            return DownloadResult(
                success=True,
                url=clean_url,
                title=title,
                filename=fpath.name if fpath else f"{title}.{preferred_format}",
                file_path=fpath,
                file_size_bytes=size,
                duration_seconds=time.time() - start,
                media_type="video",
                quality_or_format=quality,
            )
        except Exception as exc:
            return DownloadResult(
                success=False,
                url=clean_url,
                title=title,
                error_message=str(exc),
                duration_seconds=time.time() - start,
                media_type="video",
                quality_or_format=quality,
            )
        finally:
            if progress_callback:
                self.dispatcher.remove_listener(progress_callback)

    def download_audio(
        self,
        url: str,
        audio_format: str = "mp3",
        quality: str = "192",
        output_dir: Optional[Union[str, Path]] = None,
        cookies_from_browser: Optional[str] = None,
        cookies_file: Optional[str] = None,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> DownloadResult:
        start = time.time()
        target = resolve_output_path(output_dir)
        clean_url = clean_media_url(url, is_playlist=False)

        if progress_callback:
            self.dispatcher.add_listener(progress_callback)

        hook = YtdlpProgressHook(self.dispatcher)
        outtmpl = str(target / "%(title)s.%(ext)s")
        opts: Dict[str, Any] = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "progress_hooks": [hook],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "continuedl": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web", "mweb"],
                    "player_skip": ["configs", "webpage"],
                }
            },
        }
        if cookies_from_browser:
            opts["cookiesfrombrowser"] = (cookies_from_browser,)
        elif cookies_file:
            opts["cookiefile"] = cookies_file

        if self.ffmpeg.is_available:
            opts["postprocessors"] = build_audio_postprocessors(audio_format, quality=quality)
            opts["ffmpeg_location"] = self.ffmpeg.ffmpeg_path

        title = "Unknown"
        final_fn = ""
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                if info:
                    title = info.get("title", "Unknown")
                    base_fn = ydl.prepare_filename(info)
                    base, _ = os.path.splitext(base_fn)
                    expected = f"{base}.{audio_format}"
                    final_fn = expected if os.path.isfile(expected) else base_fn

            fpath = Path(final_fn) if final_fn and os.path.isfile(final_fn) else None
            size = fpath.stat().st_size if fpath and fpath.exists() else 0

            return DownloadResult(
                success=True,
                url=clean_url,
                title=title,
                filename=fpath.name if fpath else f"{title}.{audio_format}",
                file_path=fpath,
                file_size_bytes=size,
                duration_seconds=time.time() - start,
                media_type="audio",
                quality_or_format=audio_format,
            )
        except Exception as exc:
            return DownloadResult(
                success=False,
                url=clean_url,
                title=title,
                error_message=str(exc),
                duration_seconds=time.time() - start,
                media_type="audio",
                quality_or_format=audio_format,
            )
        finally:
            if progress_callback:
                self.dispatcher.remove_listener(progress_callback)

    def download_playlist(
        self,
        url: str,
        quality: str = "best",
        range_start: Optional[int] = None,
        range_end: Optional[int] = None,
        output_dir: Optional[Union[str, Path]] = None,
        cookies_from_browser: Optional[str] = None,
        cookies_file: Optional[str] = None,
        on_item_start: Optional[Callable[[int, int, str], None]] = None,
        on_item_progress: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> List[DownloadResult]:
        target = resolve_output_path(output_dir)
        clean_pl_url = normalize_playlist_url(url)

        extract_opts: Dict[str, Any] = {
            "quiet": True,
            "extract_flat": True,
            "no_warnings": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web", "mweb"],
                    "player_skip": ["configs", "webpage"],
                }
            },
        }
        if cookies_from_browser:
            extract_opts["cookiesfrombrowser"] = (cookies_from_browser,)
        elif cookies_file:
            extract_opts["cookiefile"] = cookies_file

        with YoutubeDL(extract_opts) as ydl:
            try:
                pl_info = ydl.extract_info(clean_pl_url, download=False)
            except Exception:
                pl_info = ydl.extract_info(url, download=False)

        if not pl_info or "entries" not in pl_info:
            return [self.download_video(url, quality=quality, output_dir=target, cookies_from_browser=cookies_from_browser, cookies_file=cookies_file, progress_callback=on_item_progress)]

        entries = list(pl_info.get("entries") or [])
        total = len(entries)
        s_idx = max(1, range_start or 1)
        e_idx = min(total, range_end or total)

        results: List[DownloadResult] = []
        for i in range(s_idx, e_idx + 1):
            entry = entries[i - 1]
            if not entry:
                continue
            e_url = entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={entry.get('id')}"
            e_title = entry.get("title", f"Track {i}")
            if on_item_start:
                on_item_start(i, e_idx - s_idx + 1, e_title)
            res = self.download_video(
                e_url,
                quality=quality,
                output_dir=target,
                cookies_from_browser=cookies_from_browser,
                cookies_file=cookies_file,
                progress_callback=on_item_progress,
            )
            results.append(res)
            time.sleep(1)
        return results
