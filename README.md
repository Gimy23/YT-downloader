# YT Downloader (`ytdl`)

> A professional, lightweight, cross-platform command-line media downloader and archiver built with Python 3.11+, yt-dlp, Typer, and Rich.

---

## 1. Project Introduction
**YT Downloader (`ytdl`)** is a fast, reliable, and elegant command-line application for downloading, extracting, and organizing publicly available audio and video media. It provides both an intuitive, modern interactive dashboard for casual desktop use and a full-featured, scriptable CLI suite for terminal power users and automation pipelines.

Tested and supported on:
- **Linux**: Ubuntu, Debian, Fedora, Arch Linux, openSUSE, and standard POSIX distributions.
- **Windows**: Windows 10 and Windows 11 (Command Prompt & Windows PowerShell).
- **macOS**: Sonoma, Ventura, and Monterey.
- **Shells**: Bash, Zsh, Fish, Dash, and PowerShell.

---

## 2. Features
- **High-Definition Video Retrieval**: Automatic selection of the highest quality video and audio streams with lossless merging.
- **Audio Extraction**: Fast extraction directly into **MP3**, **M4A**, **WAV**, **FLAC**, or **OPUS** formats.
- **Resolution Control**: Granular quality presets (`best`, `1080p`, `720p`, `480p`, `360p`).
- **Stream Metadata Inspection**: Inspect stream titles, durations, authors, available resolutions, and formats without initiating downloads (`ytdl info`).
- **Sequential Playlist Downloads**: Download entire playlists or select entry ranges (`--range 1-5`) with individual progress tracking.
- **Cross-Platform Directory Support**: Automatic resolution of platform video folders (`~/Videos/YT-Downloads` on Linux/macOS, `%USERPROFILE%\Videos\YT-Downloads` on Windows).
- **Persistent Local History**: Local download history tracker with status indicators and cleanup utilities (`ytdl history`).
- **Configuration Management**: Persistent user preferences for default quality, directories, audio formats, and themes (`ytdl config`).
- **Premium Terminal UI**: Interactive menus, Rich progress bars with speed, ETA, percentage, and completion cards.
- **Scripting & Automation Mode**: Dedicated `--no-ui` / `--plain` flags for headless environments and shell scripts.
- **Zero Raw Tracebacks**: User-friendly error messages for network interruptions or invalid links; debug tracebacks available via `--debug`.

---

## 3. Terminal Interface Examples

### Interactive Dashboard (`ytdl`)
```text
╭─────────────────────────────────────────────────────────────╮
│ YT DOWNLOADER v1.0.0                                        │
│ Cross-Platform Media Downloader CLI                         │
│ Built with yt-dlp • Typer • Rich                            │
╰─────────────────────────────────────────────────────────────╯

                      System Dependencies                      
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component      ┃ Status ┃ Path / Version                    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ FFmpeg Engine  │ ✔ Ready│ 5.1.4 (/usr/bin/ffmpeg)           │
│ yt-dlp Core    │ ✔ Ready│ Python Library                    │
│ Rich UI        │ ✔ Ready│ Terminal Interface                │
└────────────────┴────────┴───────────────────────────────────┘

? Main Navigation Menu:
  > 1. Download Video
    2. Download Audio
    3. Video Information
    4. Playlist Downloader
    5. Download History
    6. Settings
    7. Help and About
    8. Exit
```

### Video Download Progress (`ytdl download <URL>`)
```text
Initializing video download: https://... (1080p)
Downloading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 75% 5.2 MB/s 36.0/48.0 MB 0:00:02

╭───────────────────────────── Download Complete ──────────────────────────────╮
│    Status:  ✔ Completed Successfully                                         │
│     Title:  Sample Video Document                                            │
│  Filename:  Sample_Video_Document.mp4                                        │
│ File Size:  48.00 MB                                                         │
│  Duration:  9.2s                                                             │
│  Saved to:  /home/user/Videos/YT-Downloads                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## 4. Requirements
- **Python**: 3.11 or newer.
- **FFmpeg**: *(Recommended)* Required for merging audio/video streams at 1080p+ and transcoding audio formats.

---

## 5. Linux Installation

### Option A: Using `pipx` (Recommended)
```bash
pipx install .
```

### Option B: Using standard `pip`
```bash
python3 -m pip install --upgrade pip
python3 -m pip install .
```

### Option C: Automated Install Script
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

---

## 6. Windows Installation

### Option A: PowerShell / CMD
```powershell
py -m pip install --upgrade pip
py -m pip install .
```

### Option B: Automated PowerShell Script
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\scripts\install.ps1
```

---

## 7. Usage Examples

```bash
# 1. Launch interactive dashboard
ytdl

# 2. Quick download (direct URL shortcut)
ytdl "https://www.youtube.com/watch?v=EXAMPLE_ID"

# 3. Explicit video download with resolution preset
ytdl download "https://www.youtube.com/watch?v=EXAMPLE_ID" --quality 1080p

# 4. Extract audio track to MP3
ytdl audio "https://www.youtube.com/watch?v=EXAMPLE_ID" --format mp3

# 5. Extract audio to high-fidelity FLAC
ytdl audio "https://www.youtube.com/watch?v=EXAMPLE_ID" --format flac --quality 320

# 6. Inspect metadata without downloading
ytdl info "https://www.youtube.com/watch?v=EXAMPLE_ID"

# 7. Download playlist entries 1 through 5
ytdl playlist "https://www.youtube.com/playlist?list=PL_EXAMPLE" --range 1-5

# 8. Specify custom output destination
ytdl download "https://www.youtube.com/watch?v=EXAMPLE_ID" --output ~/Media/Archive

# 9. Headless scripting mode (plain output)
ytdl download "https://www.youtube.com/watch?v=EXAMPLE_ID" --no-ui
```

---

## 8. CLI Command Reference

| Command | Arguments / Flags | Description |
| :--- | :--- | :--- |
| `ytdl` | *(None)* | Launches the interactive visual dashboard. |
| `ytdl <URL>` | `<URL>` | Direct shortcut to download video. |
| `ytdl --version`, `-v` | | Displays application version. |
| `ytdl --help` | | Displays top-level help and command list. |
| `ytdl download <URL>` | `-q, --quality`, `-o, --output`, `-f, --format`, `--no-ui` | Downloads video stream. |
| `ytdl audio <URL>` | `-f, --format`, `-q, --quality`, `-o, --output`, `--no-ui` | Extracts audio stream (MP3, M4A, WAV, FLAC, OPUS). |
| `ytdl info <URL>` | `--no-ui` | Inspects metadata, resolutions, and formats. |
| `ytdl playlist <URL>` | `-r, --range`, `-q, --quality`, `-o, --output`, `--no-ui` | Downloads playlist entries sequentially. |
| `ytdl history` | `-c, --clear`, `--no-ui` | Lists or clears local download history records. |
| `ytdl config` | `-s, --show`, `-r, --reset`, `--set-quality`, `--set-audio`, `--set-dir` | Views or updates configuration preferences. |

---

## 9. Configuration Guide
Configuration is stored in user space:
- **Linux**: `~/.config/ytdl/config.json`
- **Windows**: `%APPDATA%\ytdl\config.json`
- **macOS**: `~/Library/Application Support/ytdl/config.json`

### View Current Settings
```bash
ytdl config --show
```

### Update Defaults
```bash
ytdl config --set-quality 1080p
ytdl config --set-audio flac
ytdl config --set-dir ~/Media/Downloads
```

### Reset to Factory Defaults
```bash
ytdl config --reset
```

---

## 10. Troubleshooting

### Issue: "FFmpeg not found"
- **Cause**: FFmpeg executable is missing from system `PATH`.
- **Solution**:
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - Fedora: `sudo dnf install ffmpeg`
  - Arch: `sudo pacman -S ffmpeg`
  - Windows: `winget install Gyan.FFmpeg`

### Issue: Network Timeout / Connection Interrupted
- **Resolution**: `ytdl` automatically enables `--continuedl` to resume partial downloads. Simply re-run the command once the network stabilizes.

### Issue: Debugging Unexpected Errors
Run with `--debug` to output full stack traces:
```bash
ytdl --debug download "URL"
```

---

## 11. Development Setup
```bash
# Clone repository
git clone https://github.com/example/ytdl.git
cd ytdl

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

---

## 12. Testing Instructions
The test suite contains 27 unit and integration tests with mocked media responses:
```bash
# Run unit tests via unittest
python3 -m unittest discover -s tests -v

# Or run via pytest (if installed)
pytest -v
```

---

## 13. Contribution Guidelines
1. Fork the repository and create a descriptive feature branch (`git checkout -b feature/improved-progress`).
2. Adhere to PEP 8 standards with type annotations.
3. Add unit test coverage in `tests/` for any new logic or commands.
4. Ensure all tests pass (`python3 -m unittest discover -s tests`).
5. Submit a clean Pull Request.

---

## 14. Legal and Responsible-Use Notice
`ytdl` is an open-source command-line media retrieval utility designed exclusively for downloading and archiving content that the user owns, has authorization to access, or is explicitly available in the public domain or under permissive licenses (such as Creative Commons). 

Users are strictly responsible for complying with all applicable copyright laws, intellectual property rights, and terms of service of any third-party media platforms. `ytdl` does not bypass DRM, paywalls, encryption schemes, or authentication restrictions.
