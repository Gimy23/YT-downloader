# ==============================================================================
# YT Downloader (ytdl) - Windows PowerShell Automated Installer
# Compatible with Windows 10, Windows 11, PowerShell 5.1+, and PowerShell Core.
# ==============================================================================
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  YT Downloader (ytdl) Windows Installer" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Check for Python
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $PythonCmd) {
    Write-Error "Python 3.11+ was not detected. Please install Python from https://python.org or winget install Python.Python.3.11"
    exit 1
}

Write-Host "[INFO] Detected Python: $($PythonCmd.Source)" -ForegroundColor Green

# Check optional FFmpeg
$FFmpegCmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($FFmpegCmd) {
    Write-Host "[INFO] FFmpeg detected: $($FFmpegCmd.Source)" -ForegroundColor Green
} else {
    Write-Host "[WARN] FFmpeg is not found in PATH. Audio format conversions will be limited." -ForegroundColor Yellow
    Write-Host "       Install via: winget install Gyan.FFmpeg" -ForegroundColor Gray
}

# Install using pipx or pip
$PipxCmd = Get-Command pipx -ErrorAction SilentlyContinue
if ($PipxCmd) {
    Write-Host "[INFO] Installing via pipx..." -ForegroundColor Cyan
    pipx install . --force
} else {
    Write-Host "[INFO] Installing via pip..." -ForegroundColor Cyan
    & $PythonCmd.Source -m pip install --upgrade .
}

Write-Host "`n[SUCCESS] YT Downloader installed successfully!" -ForegroundColor Green
Write-Host "Execute 'ytdl' in PowerShell or Command Prompt to get started." -ForegroundColor Cyan
