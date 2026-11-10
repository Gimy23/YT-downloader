"""History command."""
from ytdl.compat import Option
from ytdl.services.history_service import HistoryService
from ytdl.ui.tables import create_history_table
from ytdl.ui.themes import console, plain_console

def history_command(
    clear: bool = Option(False, "--clear", "-c", help="Clear all stored local download history"),
    no_ui: bool = Option(False, "--no-ui", "--plain", help="Output plain text"),
) -> None:
    out_console = plain_console if no_ui else console
    history = HistoryService()
    if clear:
        history.clear()
        out_console.print("[green]Download history cleared.[/green]")
        return
    items = history.get_all()
    if no_ui:
        for item in items:
            out_console.print(f"{item.date[:10]} | {item.media_type.upper():5} | {item.status.upper():9} | {item.title}")
    else:
        out_console.print(create_history_table(items))
