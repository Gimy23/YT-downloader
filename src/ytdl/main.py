"""Main execution entry point."""
from __future__ import annotations
import sys
import traceback
from ytdl.cli import app
from ytdl.ui.themes import console

KNOWN_COMMANDS = {"download", "audio", "info", "playlist", "history", "config"}

def run_cli() -> None:
    # If the user passed a URL directly, e.g. `ytdl https://...`, route to download
    if len(sys.argv) > 1:
        first = sys.argv[1]
        if (first.startswith("http://") or first.startswith("https://")) and first not in KNOWN_COMMANDS:
            sys.argv.insert(1, "download")

    debug_mode = "--debug" in sys.argv
    try:
        app()
    except SystemExit as exc:
        sys.exit(exc.code)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(130)
    except Exception as exc:
        if debug_mode:
            console.print("[bold red]Unhandled Exception occurred in debug mode:[/bold red]")
            traceback.print_exc()
        else:
            console.print(f"[bold red][ERROR] {exc}[/bold red]")
            console.print("[muted]Pass --debug for complete traceback.[/muted]")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
