"""Configuration storage service."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Optional
from ytdl.models.settings import AppConfig
from ytdl.utils.paths import get_config_dir

class ConfigService:
    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.config_dir = config_dir or get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self._config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        if self._config is not None:
            return self._config
        if self.config_file.exists():
            try:
                data = json.loads(self.config_file.read_text(encoding="utf-8"))
                self._config = AppConfig.from_dict(data)
                return self._config
            except Exception:
                pass
        self._config = AppConfig()
        return self._config

    def save(self, config: AppConfig) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
        self._config = config

    def update(self, **kwargs: Any) -> AppConfig:
        cfg = self.load()
        for k, v in kwargs.items():
            if hasattr(cfg, k) and v is not None:
                setattr(cfg, k, v)
        self.save(cfg)
        return cfg

    def reset(self) -> AppConfig:
        cfg = AppConfig()
        self.save(cfg)
        return cfg
