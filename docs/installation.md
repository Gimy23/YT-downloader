# Installation Guide for YT Downloader (ytdl)

`ytdl` is designed to be installed effortlessly across modern Linux distributions and Windows operating systems.

---

## 1. System Requirements
- **Python**: 3.11, 3.12, or higher.
- **Terminal**: Any standard terminal emulator (GNOME Terminal, Kitty, Ghostty, Alacritty, Windows Terminal, PowerShell, CMD).
- **FFmpeg** *(Optional but recommended)*: Required for high-bitrate audio extraction (MP3, FLAC, WAV, OPUS) and merging 1080p+ video streams.

---

## 2. Linux Installation

### Using pipx (Recommended for isolated CLI tools)
```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y python3-pip python3-venv pipx ffmpeg
pipx ensurepath
pipx install .

# Fedora / RHEL
sudo dnf install -y python3-pip pipx ffmpeg
pipx ensurepath
pipx install .

# Arch Linux
sudo pacman -S python-pipx ffmpeg
pipx ensurepath
pipx install .
```

### Using standard pip
```bash
python3 -m pip install --upgrade pip
python3 -m pip install .
```

### Automated Script
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

---

## 3. Windows 10 & Windows 11 Installation

### Using PowerShell
1. Open PowerShell as user.
2. Install FFmpeg (optional, recommended):
   ```powershell
   winget install Gyan.FFmpeg
   ```
3. Install `ytdl`:
   ```powershell
   py -m pip install --upgrade pip
   py -m pip install .
   ```
   Or using pipx:
   ```powershell
   pipx install .
   ```

### Automated PowerShell Script
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\scripts\install.ps1
```

---

## 4. Standalone Executable (PyInstaller)
To package a standalone executable without requiring a system Python runtime:

```bash
# On Linux
pyinstaller ytdl.spec
# Binary generated at: dist/ytdl

# On Windows
pyinstaller ytdl.spec
# Binary generated at: dist/ytdl.exe
```
