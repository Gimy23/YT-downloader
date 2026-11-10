"""Tables for history and dependencies."""
from typing import Any, Dict, List
from rich.table import Table
from ytdl.models.download import DownloadHistoryItem
from ytdl.utils.terminal import SYMBOLS

def create_history_table(items: List[DownloadHistoryItem]) -> Table:
    table = Table(title="Recent Download History", border_style="cyan", header_style="bold cyan")
    table.add_column("Date", style="muted", width=16)
    table.add_column("Type", width=8)
    table.add_column("Title", style="white")
    table.add_column("Status", width=12)

    for item in items[:15]:
        status_styled = f"[green]{SYMBOLS.SUCCESS} Done[/green]" if item.status == "completed" else f"[red]{SYMBOLS.ERROR} Failed[/red]"
        type_str = "[cyan]Audio[/cyan]" if item.media_type == "audio" else "[blue]Video[/blue]"
        dt = item.date[:10] if len(item.date) >= 10 else item.date
        table.add_row(dt, type_str, item.title[:45], status_styled)

    if not items:
        table.add_row("--", "--", "No download history found.", "--")
    return table

def create_dependency_table(deps: Dict[str, Any]) -> Table:
    table = Table(title="System Dependencies", border_style="cyan", header_style="bold cyan")
    table.add_column("Component", style="white")
    table.add_column("Status", style="bold")
    table.add_column("Path / Version", style="muted")

    ff_status = f"[green]{SYMBOLS.SUCCESS} Ready[/green]" if deps.get("available") else f"[yellow]{SYMBOLS.WARNING} Optional[/yellow]"
    table.add_row("FFmpeg Engine", ff_status, f"{deps.get('version', '')} ({deps.get('path', '')})")
    table.add_row("yt-dlp Core", f"[green]{SYMBOLS.SUCCESS} Integrated[/green]", "Python Library")
    table.add_row("Rich UI", f"[green]{SYMBOLS.SUCCESS} Active[/green]", "Terminal Interface")
    return table
