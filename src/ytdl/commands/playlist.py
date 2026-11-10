"""Playlist command."""
from typing import Optional
from ytdl.compat import Argument, Exit, Option
from ytdl.core.downloader import Downloader
from ytdl.services.config_service import ConfigService
from ytdl.services.history_service import HistoryService
from ytdl.ui.progress import InteractiveProgressUI
from ytdl.ui.themes import console, plain_console
from ytdl.utils.validators import parse_playlist_range, validate_url, validate_video_quality

def playlist_command(
    url: str = Argument(..., help="Playlist web URL"),
    quality: str = Option("best", "--quality", "-q", help="Video quality preset"),
    range: Optional[str] = Option(None, "--range", "-r", help="Entry range (e.g. 1-5 or 3)"),
    output: Optional[str] = Option(None, "--output", "-o", help="Target output directory"),
    cookies_from_browser: Optional[str] = Option(None, "--cookies-from-browser", help="Browser for cookies"),
    cookies: Optional[str] = Option(None, "--cookies", help="Path to cookies file"),
    no_ui: bool = Option(False, "--no-ui", "--plain", help="Plain output mode"),
) -> None:
    out_console = plain_console if no_ui else console
    try:
        url = validate_url(url)
        quality = validate_video_quality(quality)
        s_idx, e_idx = parse_playlist_range(range)
    except ValueError as e:
        out_console.print(f"[red]Error: {e}[/red]")
        raise Exit(code=1)

    cfg = ConfigService().load()
    target_dir = output or cfg.default_directory
    c_browser = cookies_from_browser or cfg.cookies_from_browser
    c_file = cookies or cfg.cookies_file
    progress_ui = None if no_ui else InteractiveProgressUI(description="Playlist Item")
    cb = progress_ui.update if progress_ui else None

    def on_item(idx: int, total: int, title: str) -> None:
        out_console.print(f"\n[cyan][{idx}/{total}][/cyan] [white]{title}[/white]")

    downloader = Downloader()
    results = downloader.download_playlist(url=url, quality=quality, range_start=s_idx, range_end=e_idx, output_dir=target_dir, cookies_from_browser=c_browser, cookies_file=c_file, on_item_start=on_item, on_item_progress=cb)
    if progress_ui:
        progress_ui.stop()

    success_cnt = sum(1 for r in results if r.success)
    out_console.print(f"\n[bold green]Playlist summary: {success_cnt}/{len(results)} downloaded successfully.[/bold green]")
    folder_str = ""
    for r in results:
        if r.file_path:
            folder_str = str(r.file_path.parent)
            break
    if folder_str:
        out_console.print(f"Saved to: [bold cyan]{folder_str}[/bold cyan]")
