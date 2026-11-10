"""Info command."""
from ytdl.compat import Argument, Exit, Option
from ytdl.core.extractor import MediaExtractor
from ytdl.ui.panels import create_error_panel, create_info_panel
from ytdl.ui.themes import console, plain_console
from ytdl.utils.validators import validate_url

def info_command(
    url: str = Argument(..., help="Media stream URL to inspect"),
    no_ui: bool = Option(False, "--no-ui", "--plain", help="Output plain text metadata"),
) -> None:
    out_console = plain_console if no_ui else console
    try:
        url = validate_url(url)
    except ValueError as e:
        out_console.print(f"[red]Error: {e}[/red]")
        raise Exit(code=1)

    extractor = MediaExtractor()
    try:
        info = extractor.extract(url)
        if no_ui:
            out_console.print(f"Title: {info.title}")
            out_console.print(f"Author: {info.uploader}")
            out_console.print(f"Duration: {info.formatted_duration}")
            out_console.print(f"Resolutions: {', '.join(info.available_resolutions)}")
            out_console.print(f"URL: {info.webpage_url}")
        else:
            out_console.print(create_info_panel(info))
    except Exception as exc:
        if no_ui:
            out_console.print(f"ERROR: {exc}")
        else:
            out_console.print(create_error_panel("Metadata Inspection Failed", reason=str(exc)))
        raise Exit(code=1)
