"""Interactive Dashboard Home Screen."""
from ytdl import __version__
from ytdl.core.downloader import Downloader
from ytdl.core.extractor import MediaExtractor
from ytdl.services.config_service import ConfigService
from ytdl.services.ffmpeg_service import FFmpegService
from ytdl.services.history_service import HistoryService
from ytdl.ui.menus import (
    handle_audio_download,
    handle_history_menu,
    handle_info_inspection,
    handle_playlist_download,
    handle_settings_menu,
    handle_video_download,
)
from ytdl.ui.panels import create_header_panel
from ytdl.ui.prompts import prompt_select
from ytdl.ui.tables import create_dependency_table
from ytdl.ui.themes import console

def run_dashboard() -> None:
    downloader = Downloader()
    extractor = MediaExtractor()
    history = HistoryService()
    config = ConfigService()
    ffmpeg = FFmpegService()

    console.clear()
    console.print(create_header_panel(__version__))
    console.print(create_dependency_table(ffmpeg.get_status()))

    choices = [
        "1. Download Video",
        "2. Download Audio",
        "3. Video Information",
        "4. Playlist Downloader",
        "5. Download History",
        "6. Settings",
        "7. Help and About",
        "8. Exit",
    ]

    action = prompt_select("Main Navigation Menu", choices=choices)
    if action.startswith("1"):
        handle_video_download(downloader, history, config)
    elif action.startswith("2"):
        handle_audio_download(downloader, history, config)
    elif action.startswith("3"):
        handle_info_inspection(extractor)
    elif action.startswith("4"):
        handle_playlist_download(downloader, history, config)
    elif action.startswith("5"):
        handle_history_menu(history)
    elif action.startswith("6"):
        handle_settings_menu(config)
    elif action.startswith("7"):
        console.print("\n[bold cyan]About YT Downloader[/bold cyan]")
        console.print("Cross-platform command-line media retrieval tool.")
        console.print("Usage: ytdl download <URL> | ytdl audio <URL> | ytdl info <URL>\n")
    elif action.startswith("8"):
        console.print("\n[cyan]Thank you for using YT Downloader![/cyan]")
