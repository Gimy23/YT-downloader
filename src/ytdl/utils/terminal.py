"""Terminal output capabilities and ASCII/Unicode symbols."""
from __future__ import annotations
import os
import shutil
import sys

def supports_color() -> bool:
    if os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb":
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    return True

def supports_unicode() -> bool:
    enc = getattr(sys.stdout, "encoding", None) or "ascii"
    return "utf" in enc.lower()

class Symbols:
    def __init__(self, u: bool = True):
        self.u = u
    @property
    def SUCCESS(self) -> str: return "✔" if self.u else "[OK]"
    @property
    def ERROR(self) -> str: return "✖" if self.u else "[ERROR]"
    @property
    def WARNING(self) -> str: return "⚠" if self.u else "[WARN]"

SYMBOLS = Symbols(u=supports_unicode())
