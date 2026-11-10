"""Config command."""
from typing import Optional
from rich.table import Table
from ytdl.compat import Option
from ytdl.services.config_service import ConfigService
from ytdl.ui.themes import console, plain_console

def config_command(
    show: bool = Option(False, "--show", "-s", help="Display current configuration values"),
    reset: bool = Option(False, "--reset", "-r", help="Reset settings to factory defaults"),
    set_dir: Optional[str] = Option(None, "--set-dir", help="Set default download directory"),
    set_quality: Optional[str] = Option(None, "--set-quality", help="Set default video quality"),
    set_audio: Optional[str] = Option(None, "--set-audio", help="Set default audio format"),
    set_cookies_browser: Optional[str] = Option(None, "--set-cookies-browser", help="Set default browser for cookies (firefox, chrome, brave, edge)"),
    no_ui: bool = Option(False, "--no-ui", "--plain", help="Output plain text"),
) -> None:
    out_console = plain_console if no_ui else console
    service = ConfigService()
    if reset:
        service.reset()
        out_console.print("[green]Configuration reset to defaults.[/green]")
        return
    if set_dir or set_quality or set_audio or set_cookies_browser:
        service.update(default_directory=set_dir, default_video_quality=set_quality, default_audio_format=set_audio)
        out_console.print("[green]Configuration updated successfully.[/green]")
        return
    cfg = service.load()
    if no_ui:
        for k, v in cfg.to_dict().items():
            out_console.print(f"{k} = {v}")
    else:
        tbl = Table(title="Application Configuration", border_style="cyan", header_style="bold cyan")
        tbl.add_column("Key", style="bold white")
        tbl.add_column("Value", style="cyan")
        for k, v in cfg.to_dict().items():
            tbl.add_row(k, str(v))
        out_console.print(tbl)
