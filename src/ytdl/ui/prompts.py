"""Interactive prompt abstractions with Questionary & Rich fallback."""
from typing import List, Optional
from ytdl.compat import HAS_QUESTIONARY, questionary
from ytdl.ui.themes import console

def prompt_text(message: str, default: str = "") -> str:
    if HAS_QUESTIONARY and questionary:
        try:
            ans = questionary.text(message, default=default).ask()
            return (ans or "").strip()
        except KeyboardInterrupt:
            return ""
    def_str = f" [{default}]" if default else ""
    console.print(f"[bold cyan]? {message}{def_str}:[/bold cyan] ", end="")
    try:
        val = input().strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        return ""

def prompt_select(message: str, choices: List[str], default: Optional[str] = None) -> str:
    if HAS_QUESTIONARY and questionary:
        try:
            ans = questionary.select(message, choices=choices, default=default).ask()
            return ans or ""
        except KeyboardInterrupt:
            return ""

    console.print(f"\n[bold cyan]? {message}[/bold cyan]")
    for idx, choice in enumerate(choices, 1):
        marker = ">" if choice == default else " "
        console.print(f"  {marker} [bold white]{idx}.[/bold white] {choice}")

    while True:
        console.print("[bold cyan]Enter choice number (or 0 to cancel):[/bold cyan] ", end="")
        try:
            raw = input().strip()
            if raw == "0" or raw.lower() in ("q", "b", "back", "exit"):
                return ""
            if not raw and default:
                return default
            num = int(raw)
            if 1 <= num <= len(choices):
                return choices[num - 1]
        except (ValueError, EOFError, KeyboardInterrupt):
            return ""
        console.print("[yellow]Please enter a valid choice number.[/yellow]")

def prompt_confirm(message: str, default: bool = True) -> bool:
    if HAS_QUESTIONARY and questionary:
        try:
            ans = questionary.confirm(message, default=default).ask()
            return bool(ans) if ans is not None else False
        except KeyboardInterrupt:
            return False
    def_str = "Y/n" if default else "y/N"
    console.print(f"[bold cyan]? {message} ({def_str}):[/bold cyan] ", end="")
    try:
        ans = input().strip().lower()
        if not ans:
            return default
        return ans in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False
