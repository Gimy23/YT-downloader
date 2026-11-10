# YT Downloader Architecture & Design

## Architectural Principles
1. **Decoupled Downloader & UI**: The core downloading engine (`ytdl.core.downloader`) produces structured events (`DownloadProgress`, `DownloadResult`). It never prints directly to `stdout`. UI consumers (Rich interactive progress or plain text) subscribe to these events.
2. **Cross-Platform Path Resolution**: All path handling uses `pathlib.Path` with platform-specific defaults:
   - Linux: `~/Videos/YT-Downloads`, `~/.config/ytdl`, `~/.local/share/ytdl`
   - Windows: `%USERPROFILE%\Videos\YT-Downloads`, `%APPDATA%\ytdl`, `%LOCALAPPDATA%\ytdl`
3. **Graceful Degradation**:
   - Falls back gracefully when FFmpeg is not installed.
   - Falls back to plain ASCII and no-color when running in dumb or redirected terminals.
   - Dual execution modes: interactive rich dashboard (`ytdl`) and scriptable CLI (`ytdl download URL --no-ui`).
4. **Legal & Compliance Guardrails**: Extracts publicly available media streams and respects access controls without DRM bypass.

## Component Layout
- `ytdl.main`: Entry point with exception shielding and debug mode routing.
- `ytdl.cli`: Typer application registering subcommands.
- `ytdl.compat`: Compatibility layer adapting Typer/Click, yt-dlp, and Questionary.
- `ytdl.core`: Downloader, Extractor, Formats, and Progress dispatcher.
- `ytdl.services`: ConfigService, HistoryService, FFmpegService.
- `ytdl.ui`: Themes, Panels, Tables, Progress, Prompts, Dashboard.
- `ytdl.utils`: Paths, Validators, Terminal helpers.
