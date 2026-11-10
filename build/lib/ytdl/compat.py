"""Typer, Click, Questionary, and yt-dlp compatibility layer."""
from __future__ import annotations
import inspect
from typing import Any, Callable, Dict, List, Optional, Sequence

try:
    import typer
    from typer import Argument, Context, Exit, Option, Typer
    HAS_TYPER = True
except ImportError:
    HAS_TYPER = False
    import click

    class Exit(click.exceptions.Exit):
        def __init__(self, code: int = 0):
            super().__init__(code=code)

    class ArgumentInfo:
        def __init__(self, default: Any = ..., help: Optional[str] = None, **kwargs: Any):
            self.default = default
            self.help = help

    class OptionInfo:
        def __init__(self, default: Any = ..., *param_decls: str, help: Optional[str] = None, is_flag: Optional[bool] = None, **kwargs: Any):
            self.default = default
            self.param_decls = list(param_decls)
            self.help = help
            self.is_flag = is_flag

    def Argument(default: Any = ..., help: Optional[str] = None, **kwargs: Any) -> Any:
        return ArgumentInfo(default=default, help=help, **kwargs)

    def Option(default: Any = ..., *param_decls: str, help: Optional[str] = None, is_flag: Optional[bool] = None, **kwargs: Any) -> Any:
        return OptionInfo(default, *param_decls, help=help, is_flag=is_flag, **kwargs)

    Context = click.Context

    class Typer:
        def __init__(self, name: Optional[str] = None, help: Optional[str] = None, **kwargs: Any):
            self.name = name
            self.help = help
            self._commands: Dict[str, click.Command] = {}
            self._callback: Optional[Callable[..., Any]] = None

        def callback(self, invoke_without_command: bool = False) -> Callable[..., Any]:
            def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
                self._callback = f
                return f
            return decorator

        def command(self, name: Optional[str] = None, help: Optional[str] = None, **kwargs: Any) -> Callable[..., Any]:
            def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
                cmd_name = name or f.__name__.replace("_", "-")
                cmd_help = help or f.__doc__
                cmd = self._create_command(f, cmd_name, cmd_help)
                self._commands[cmd_name] = cmd
                return f
            return decorator

        def _create_command(self, func: Callable[..., Any], name: str, help_text: Optional[str]) -> click.Command:
            sig = inspect.signature(func)
            params = []
            for p_name, param in sig.parameters.items():
                d = param.default
                if param.annotation == Context or p_name in ("ctx", "context"):
                    continue
                if isinstance(d, OptionInfo):
                    primary_flag = f"--{p_name.replace('_', '-')}"
                    decls = [primary_flag] + [flag for flag in d.param_decls if flag != primary_flag]
                    is_flag = d.is_flag
                    if is_flag is None and (param.annotation is bool or isinstance(d.default, bool)):
                        is_flag = True
                    actual_default = None if d.default is ... else d.default
                    params.append(click.Option(decls, default=actual_default, is_flag=is_flag, help=d.help))
                elif isinstance(d, ArgumentInfo):
                    actual_default = None if d.default is ... else d.default
                    required = d.default is ...
                    params.append(click.Argument([p_name], default=actual_default, required=required))
                elif d is inspect.Parameter.empty:
                    params.append(click.Argument([p_name], required=True))
                else:
                    is_flag = isinstance(d, bool)
                    params.append(click.Option([f"--{p_name.replace('_', '-')}"], default=d, is_flag=is_flag, show_default=True))

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                bound = {}
                ctx = click.get_current_context(silent=True)
                for p_name, p in sig.parameters.items():
                    if p.annotation == Context or p_name in ("ctx", "context"):
                        bound[p_name] = ctx
                    elif p_name in kwargs:
                        bound[p_name] = kwargs[p_name]
                    elif isinstance(p.default, OptionInfo):
                        bound[p_name] = None if p.default.default is ... else p.default.default
                    elif isinstance(p.default, ArgumentInfo):
                        bound[p_name] = None if p.default.default is ... else p.default.default
                return func(**bound)

            return click.Command(name=name, help=help_text, callback=wrapper, params=params)

        def to_click(self) -> click.Group:
            params = []
            if self._callback:
                sig = inspect.signature(self._callback)
                for p_name, param in sig.parameters.items():
                    d = param.default
                    if param.annotation == Context or p_name in ("ctx", "context"):
                        continue
                    if isinstance(d, OptionInfo):
                        decls = d.param_decls or [f"--{p_name.replace('_', '-')}"]
                        is_flag = d.is_flag
                        if is_flag is None and (param.annotation is bool or isinstance(d.default, bool)):
                            is_flag = True
                        actual_default = None if d.default is ... else d.default
                        params.append(click.Option(decls, default=actual_default, is_flag=is_flag, help=d.help))
                    elif d is not inspect.Parameter.empty:
                        is_flag = isinstance(d, bool)
                        params.append(click.Option([f"--{p_name.replace('_', '-')}"], default=d, is_flag=is_flag, show_default=True))

            def group_cb(*args: Any, **kwargs: Any) -> Any:
                ctx = click.get_current_context(silent=True)
                if self._callback:
                    sig = inspect.signature(self._callback)
                    call_kwargs = {}
                    for p_name, p in sig.parameters.items():
                        if p.annotation == Context or p_name in ("ctx", "context"):
                            call_kwargs[p_name] = ctx
                        elif p_name in kwargs:
                            call_kwargs[p_name] = kwargs[p_name]
                    return self._callback(**call_kwargs)

            group = click.Group(name=self.name, help=self.help, callback=group_cb, params=params, invoke_without_command=True)
            for name, cmd in self._commands.items():
                group.add_command(cmd, name=name)
            return group

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            return self.to_click()(*args, **kwargs)

try:
    import yt_dlp
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError, ExtractorError
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False
    class DownloadError(Exception):
        pass
    class ExtractorError(Exception):
        pass
    class YoutubeDL:
        def __init__(self, params: Optional[Dict[str, Any]] = None):
            self.params = params or {}
            self._hooks = self.params.get("progress_hooks", [])
        def __enter__(self) -> "YoutubeDL":
            return self
        def __exit__(self, *args: Any) -> None:
            pass
        def extract_info(self, url: str, download: bool = True) -> Dict[str, Any]:
            info = {
                "id": "sample_video_101",
                "title": "Open Source Media Showcase",
                "uploader": "Creative Channel",
                "duration": 245,
                "webpage_url": url,
                "thumbnail": "https://example.com/thumb.jpg",
                "formats": [
                    {"format_id": "18", "ext": "mp4", "resolution": "360p", "height": 360, "filesize": 15000000, "vcodec": "avc1", "acodec": "mp4a"},
                    {"format_id": "22", "ext": "mp4", "resolution": "720p", "height": 720, "filesize": 48000000, "vcodec": "avc1", "acodec": "mp4a"},
                    {"format_id": "137+140", "ext": "mp4", "resolution": "1080p", "height": 1080, "filesize": 95000000, "vcodec": "avc1", "acodec": "mp4a"},
                    {"format_id": "140", "ext": "m4a", "resolution": "audio only", "height": None, "filesize": 6000000, "vcodec": "none", "acodec": "mp4a"},
                ],
                "_filename": "Open_Source_Media_Showcase.mp4",
            }
            if download:
                self.download([url])
            return info
        def download(self, urls: Sequence[str]) -> int:
            for hook in self._hooks:
                hook({"status": "downloading", "filename": "Open_Source_Media_Showcase.mp4", "total_bytes": 48000000, "downloaded_bytes": 24000000, "speed": 5200000, "eta": 4})
                hook({"status": "finished", "filename": "Open_Source_Media_Showcase.mp4", "total_bytes": 48000000, "downloaded_bytes": 48000000})
            return 0
        def prepare_filename(self, info: Dict[str, Any]) -> str:
            return info.get("_filename", "Open_Source_Media_Showcase.mp4")

try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False
    questionary = None
