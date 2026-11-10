"""Audio command."""
from typing import Optional
from ytdl.compat import Argument, Exit, Option
from ytdl.core.downloader import Downloader
from ytdl.services.config_service import ConfigService
from ytdl.services.history_service import HistoryService
from ytdl.ui.panels import create_completion_panel, create_error_panel
from ytdl.ui.progress import InteractiveProgressUI
from ytdl.ui.themes import console, plain_console
from ytdl.utils.validators import validate_audio_format, validate_url

def audio_command(
    url: str = Argument(..., help="Media stream or video URL"),
    format: str = Option("mp3", "--format", "-f", help="Audio target format (mp3, m4a, wav, flac, opus)"),
    quality: str = Option("192", "--quality", "-q", help="Audio bitrate quality (e.g. 192, 256, 320)"),
    output: Optional[str] = Option(None, "--output", "-o", help="Target output directory"),
    cookies_from_browser: Optional[str] = Option(None, "--cookies-from-browser", help="Load cookies from browser (chrome, firefox, brave, edge, chromium)"),
    cookies: Optional[str] = Option(None, "--cookies", help="Path to cookies file"),
    no_ui: bool = Option(False, "--no-ui", "--plain", help="Disable rich panels and output plain text"),
) -> None:
    out_console = plain_console if no_ui else console
    try:
        url = validate_url(url)
        format = validate_audio_format(format)
    except ValueError as e:
        out_console.print(f"[red]Error: {e}[/red]")
        raise Exit(code=1)

    cfg = ConfigService().load()
    target_dir = output or cfg.default_directory
    c_browser = cookies_from_browser or cfg.cookies_from_browser
    c_file = cookies or cfg.cookies_file

    progress_ui = None if no_ui else InteractiveProgressUI(description="Extracting Audio")
    cb = progress_ui.update if progress_ui else None

    if not no_ui:
        out_console.print(f"[cyan]Initializing audio extraction: {url} ({format.upper()})[/cyan]")

    downloader = Downloader()
    result = downloader.download_audio(url=url, audio_format=format, quality=quality, output_dir=target_dir, progress_callback=cb)
    if progress_ui:
        progress_ui.stop()

    if result.success:
        if no_ui:
            out_console.print(f"SUCCESS: {result.filename} ({result.file_size_human}) -> {result.file_path}")
        else:
            out_console.print(create_completion_panel(result))
        HistoryService().add(title=result.title, url=url, filename=result.filename or "", output_path=str(result.file_path) if result.file_path else "", status="completed", media_type="audio", file_size_bytes=result.file_size_bytes)
    else:
        if no_ui:
            out_console.print(f"ERROR: {result.error_message}")
        else:
            out_console.print(create_error_panel(result.error_message or "Audio download failed."))
        raise Exit(code=1)
