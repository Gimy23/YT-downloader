"""Live interactive progress renderer."""
from typing import Any, Optional
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from ytdl.models.download import DownloadProgress
from ytdl.ui.themes import console

class InteractiveProgressUI:
    def __init__(self, description: str = "Downloading") -> None:
        self.progress = Progress(
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            BarColumn(complete_style="cyan", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TransferSpeedColumn(),
            DownloadColumn(),
            TimeRemainingColumn(),
            console=console,
            transient=False,
        )
        self.task_id: Optional[Any] = None

    def start(self, total_bytes: int = 0) -> None:
        self.progress.start()
        self.task_id = self.progress.add_task("Downloading", total=total_bytes or 100)

    def update(self, prog: DownloadProgress) -> None:
        if self.task_id is None:
            self.start(prog.total_bytes)
        if prog.total_bytes and prog.total_bytes > 0:
            self.progress.update(self.task_id, total=prog.total_bytes, completed=prog.downloaded_bytes)
        else:
            self.progress.update(self.task_id, completed=prog.percentage)

    def stop(self) -> None:
        try:
            self.progress.stop()
        except Exception:
            pass
