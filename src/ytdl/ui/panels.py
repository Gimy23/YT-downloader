"""Terminal rendering panels."""
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ytdl.models.download import DownloadResult, VideoInfo
from ytdl.utils.terminal import SYMBOLS

def create_header_panel(version: str = "1.0.0") -> Panel:
    text = Text()
    text.append("YT DOWNLOADER ", style="bold cyan")
    text.append(f"v{version}\n", style="dim cyan")
    text.append("Cross-Platform Media Downloader CLI\n", style="secondary")
    text.append("Built with yt-dlp • Typer • Rich", style="muted")
    return Panel(text, border_style="cyan", padding=(1, 2))

def create_info_panel(info: VideoInfo) -> Panel:
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="right")
    table.add_column(style="white")
    table.add_row("Title:", info.title)
    table.add_row("Author:", info.uploader)
    table.add_row("Duration:", info.formatted_duration)
    res_list = ", ".join(info.available_resolutions[:6]) or "Standard resolutions"
    table.add_row("Resolutions:", res_list)
    return Panel(table, title="[bold cyan]Media Information[/bold cyan]", border_style="cyan")

def create_completion_panel(result: DownloadResult) -> Panel:
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold green", justify="right")
    table.add_column(style="white")
    table.add_row("Status:", f"{SYMBOLS.SUCCESS} Completed Successfully")
    table.add_row("Title:", result.title or "Media File")
    table.add_row("Filename:", result.filename or "media")
    table.add_row("File Size:", result.file_size_human)
    table.add_row("Duration:", f"{result.duration_seconds:.1f}s")
    if result.file_path:
        table.add_row("Saved to:", str(result.file_path.parent))
    return Panel(table, title="[bold green]Download Complete[/bold green]", border_style="green")

def create_error_panel(msg: str, reason: str = "") -> Panel:
    text = Text()
    text.append(f"{SYMBOLS.ERROR} [ERROR] {msg}\n\n", style="bold red")
    if "Sign in to confirm" in reason or "not a bot" in reason:
        text.append("YouTube anti-bot challenge detected.\n\n", style="bold yellow")
        text.append("Quick Resolution:\n", style="bold cyan")
        text.append("Pass cookies from your local web browser using:\n", style="white")
        text.append("  ytdl download \"<URL>\" --cookies-from-browser firefox\n", style="bold green")
        text.append("  (or chrome, brave, edge, chromium)\n\n", style="secondary")
        text.append("Or save your browser preference permanently:\n", style="white")
        text.append("  ytdl config --set-cookies-browser firefox\n", style="bold green")
    else:
        if reason:
            text.append(f"Reason: {reason}\n\n", style="yellow")
        text.append("Suggestions:\n", style="bold white")
        text.append("• Verify your network connection and URL format.\n", style="secondary")
        text.append("• Ensure media is accessible and authorized.\n", style="secondary")
        text.append("• Pass --debug for verbose logs.", style="muted")
    return Panel(text, title="[bold red]Operation Failed[/bold red]", border_style="red")
