"""CLI Typer application definition."""
from __future__ import annotations
import sys
from typing import Optional
from ytdl import __app_name__, __version__
from ytdl.commands.audio import audio_command
from ytdl.commands.config import config_command
from ytdl.commands.download import download_command
from ytdl.commands.history import history_command
from ytdl.commands.info import info_command
from ytdl.commands.playlist import playlist_command
from ytdl.compat import Context, Exit, Option, Typer
from ytdl.ui.dashboard import run_dashboard
from ytdl.ui.themes import console

app = Typer(
    name=__app_name__,
    help="YT Downloader (ytdl) - Professional, lightweight, cross-platform media downloader.",
    add_completion=False,
)

app.command("download", help="Download a video at highest compatible quality.")(download_command)
app.command("audio", help="Extract and download audio stream.")(audio_command)
app.command("info", help="Inspect media metadata and available formats.")(info_command)
app.command("playlist", help="Download playlist entries sequentially.")(playlist_command)
app.command("history", help="Inspect or clear local download history.")(history_command)
app.command("config", help="View or modify user configuration preferences.")(config_command)

@app.callback(invoke_without_command=True)
def main_callback(
    ctx: Context,
    version: bool = Option(False, "--version", "-v", help="Display ytdl version and exit.", is_flag=True),
    debug: bool = Option(False, "--debug", help="Enable verbose debug tracebacks.", is_flag=True),
) -> None:
    if version:
        console.print(f"[bold cyan]{__app_name__}[/bold cyan] version [bold white]{__version__}[/bold white]")
        raise Exit(code=0)

    invoked_subcommand = getattr(ctx, "invoked_subcommand", None)
    if not invoked_subcommand:
        args = sys.argv[1:]
        non_flag_args = [a for a in args if not a.startswith("-")]
        if not non_flag_args:
            run_dashboard()
            raise Exit(code=0)
        elif len(non_flag_args) == 1 and (non_flag_args[0].startswith("http://") or non_flag_args[0].startswith("https://")):
            download_command(url=non_flag_args[0])
            raise Exit(code=0)
