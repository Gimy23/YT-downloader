"""Rich styling theme."""
from rich.console import Console
from rich.theme import Theme

APP_THEME = Theme({
    "primary": "bold cyan",
    "secondary": "dim white",
    "accent": "turquoise2",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "muted": "bright_black",
})

console = Console(theme=APP_THEME)
plain_console = Console(theme=APP_THEME, no_color=True)
