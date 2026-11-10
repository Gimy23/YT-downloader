"""Submenu handlers."""
from ytdl.core.downloader import Downloader
from ytdl.core.extractor import MediaExtractor
from ytdl.services.config_service import ConfigService
from ytdl.services.history_service import HistoryService
from ytdl.ui.panels import create_completion_panel, create_error_panel, create_info_panel
from ytdl.ui.progress import InteractiveProgressUI
from ytdl.ui.prompts import prompt_confirm, prompt_select, prompt_text
from ytdl.ui.tables import create_history_table
from ytdl.ui.themes import console
from ytdl.utils.validators import validate_url

def handle_video_download(downloader: Downloader, history: HistoryService, config: ConfigService) -> None:
    console.print("\n[bold cyan]─── Download Video ───[/bold cyan]")
    url = prompt_text("Enter video URL")
    if not url: return
    try: url = validate_url(url)
    except ValueError as e:
        console.print(f"[red]{e}[/red]"); return
    cfg = config.load()
    quality = prompt_select("Select video quality", ["best", "1080p", "720p", "480p", "360p"], default=cfg.default_video_quality)
    out_dir = prompt_text("Output directory (blank for default)", default=cfg.default_directory or "")

    progress_ui = InteractiveProgressUI(description="Downloading Video")
    console.print("\n[cyan]Starting video retrieval...[/cyan]")
    res = downloader.download_video(url, quality=quality, output_dir=out_dir or None, cookies_from_browser=cfg.cookies_from_browser, cookies_file=cfg.cookies_file, progress_callback=progress_ui.update)
    progress_ui.stop()

    if res.success:
        console.print(create_completion_panel(res))
        history.add(title=res.title, url=url, filename=res.filename or "", output_path=str(res.file_path) if res.file_path else "", status="completed", media_type="video", file_size_bytes=res.file_size_bytes)
    else:
        console.print(create_error_panel(res.error_message or "Download failed."))

def handle_audio_download(downloader: Downloader, history: HistoryService, config: ConfigService) -> None:
    console.print("\n[bold cyan]─── Download Audio ───[/bold cyan]")
    url = prompt_text("Enter media URL")
    if not url: return
    try: url = validate_url(url)
    except ValueError as e:
        console.print(f"[red]{e}[/red]"); return
    cfg = config.load()
    fmt = prompt_select("Select audio format", ["mp3", "m4a", "wav", "flac", "opus"], default=cfg.default_audio_format)
    out_dir = prompt_text("Output directory (blank for default)", default=cfg.default_directory or "")

    progress_ui = InteractiveProgressUI(description="Extracting Audio")
    console.print("\n[cyan]Starting audio extraction...[/cyan]")
    res = downloader.download_audio(url, audio_format=fmt, output_dir=out_dir or None, cookies_from_browser=cfg.cookies_from_browser, cookies_file=cfg.cookies_file, progress_callback=progress_ui.update)
    progress_ui.stop()

    if res.success:
        console.print(create_completion_panel(res))
        history.add(title=res.title, url=url, filename=res.filename or "", output_path=str(res.file_path) if res.file_path else "", status="completed", media_type="audio", file_size_bytes=res.file_size_bytes)
    else:
        console.print(create_error_panel(res.error_message or "Audio download failed."))

def handle_info_inspection(extractor: MediaExtractor) -> None:
    console.print("\n[bold cyan]─── Media Information ───[/bold cyan]")
    url = prompt_text("Enter video URL to inspect")
    if not url: return
    try: url = validate_url(url)
    except ValueError as e:
        console.print(f"[red]{e}[/red]"); return
    console.print("[cyan]Fetching stream metadata...[/cyan]")
    try:
        info = extractor.extract(url)
        console.print(create_info_panel(info))
    except Exception as exc:
        console.print(create_error_panel("Metadata Inspection Failed", reason=str(exc)))

def handle_playlist_download(downloader: Downloader, history: HistoryService, config: ConfigService) -> None:
    console.print("\n[bold cyan]─── Playlist Downloader ───[/bold cyan]")
    url = prompt_text("Enter playlist URL")
    if not url: return
    try: url = validate_url(url)
    except ValueError as e:
        console.print(f"[red]{e}[/red]"); return
    rng = prompt_text("Entry range (e.g. 1-5, blank for all)")
    cfg = config.load()
    quality = prompt_select("Select quality", ["best", "1080p", "720p", "480p"], default=cfg.default_video_quality)
    out_dir = prompt_text("Output directory (blank for default)", default=cfg.default_directory or "")

    from ytdl.utils.validators import parse_playlist_range
    s_idx, e_idx = parse_playlist_range(rng) if rng else (None, None)

    console.print(f"\n[cyan]Starting playlist download...[/cyan]")
    progress_ui = InteractiveProgressUI(description="Playlist Item")
    results = downloader.download_playlist(
        url, quality=quality, range_start=s_idx, range_end=e_idx, output_dir=out_dir or None, cookies_from_browser=cfg.cookies_from_browser, cookies_file=cfg.cookies_file,
        on_item_start=lambda i, tot, title: console.print(f"\n[bold cyan][Item {i}/{tot}][/bold cyan] {title}"),
        on_item_progress=progress_ui.update,
    )
    progress_ui.stop()
    success_cnt = sum(1 for r in results if r.success)
    console.print(f"\n[bold green]Playlist summary: {success_cnt}/{len(results)} items downloaded successfully.[/bold green]")
    folder_str = ""
    for r in results:
        if r.file_path:
            folder_str = str(r.file_path.parent)
            break
    if folder_str:
        console.print(f"Saved in playlist folder: [bold cyan]{folder_str}[/bold cyan]")

def handle_history_menu(history: HistoryService) -> None:
    items = history.get_all()
    console.print(create_history_table(items))
    if items and prompt_confirm("Clear download history?", default=False):
        history.clear()
        console.print("[green]Download history cleared.[/green]")

def handle_settings_menu(config: ConfigService) -> None:
    cfg = config.load()
    console.print("\n[bold cyan]─── Settings & Preferences ───[/bold cyan]")
    choice = prompt_select(
        "Choose setting",
        [
            f"Default Video Quality ({cfg.default_video_quality})",
            f"Default Audio Format ({cfg.default_audio_format})",
            f"Default Directory ({cfg.default_directory or 'System Default'})",
            f"Browser Cookies ({cfg.cookies_from_browser or 'None'})",
            "Reset All Settings to Default",
            "Back to Main Menu",
        ],
    )
    if "Video Quality" in choice:
        q = prompt_select("Default quality", ["best", "1080p", "720p", "480p", "360p"], default=cfg.default_video_quality)
        config.update(default_video_quality=q)
        console.print("[green]Default video quality updated.[/green]")
    elif "Audio Format" in choice:
        af = prompt_select("Default audio format", ["mp3", "m4a", "wav", "flac", "opus"], default=cfg.default_audio_format)
        config.update(default_audio_format=af)
        console.print("[green]Default audio format updated.[/green]")
    elif "Default Directory" in choice:
        d = prompt_text("Enter directory path", default=cfg.default_directory or "")
        config.update(default_directory=d or None)
        console.print("[green]Default download directory updated.[/green]")
    elif "Browser Cookies" in choice:
        b = prompt_select("Select browser to load cookies from", ["none", "firefox", "chrome", "brave", "edge", "chromium"])
        config.update(cookies_from_browser=None if b == "none" else b)
        console.print(f"[green]Browser cookie preference set to: {b}[/green]")
    elif "Reset" in choice and prompt_confirm("Reset all settings to defaults?"):
        config.reset()
        console.print("[green]Settings reset to factory defaults.[/green]")
