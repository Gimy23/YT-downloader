#!/usr/bin/env bash
# ==============================================================================
# YT Downloader (ytdl) - Linux & macOS Automated Installer
# Supports Ubuntu, Debian, Fedora, Arch, and generic POSIX distributions.
# ==============================================================================
set -euo pipefail

echo "=============================================="
echo "  YT Downloader (ytdl) Installer"
echo "=============================================="

# Check Python 3.11+
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 was not found in PATH."
    echo "Please install Python 3.11 or later using your package manager."
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[INFO] Detected Python $PY_VERSION"

# Check optional FFmpeg
if command -v ffmpeg &>/dev/null; then
    FF_VER=$(ffmpeg -version | head -n1 | awk '{print $3}')
    echo "[INFO] FFmpeg detected: version $FF_VER"
else
    echo "[WARN] FFmpeg not found. Video/audio merging will use stream fallbacks."
    echo "       Install FFmpeg for audio conversion: sudo apt install ffmpeg / sudo dnf install ffmpeg"
fi

# Prefer pipx if installed
if command -v pipx &>/dev/null; then
    echo "[INFO] Installing via pipx..."
    pipx install . --force
    echo "[SUCCESS] ytdl installed via pipx!"
else
    echo "[INFO] Installing via python3 -m pip install..."
    python3 -m pip install --upgrade .
    echo "[SUCCESS] ytdl installed via pip!"
fi

echo ""
echo "Run 'ytdl' to launch the interactive dashboard, or 'ytdl --help' for CLI options."
