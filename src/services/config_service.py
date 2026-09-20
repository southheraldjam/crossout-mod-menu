"""
Configuration service loading application settings and default
feature list from the bundled config files under src/config.
"""
from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, Any

import yaml

log = logging.getLogger("services.config_service")

_CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"


class ConfigService:
    def __init__(self):
        self._settings: Dict[str, Any] = {}
        self._feature_defaults: Dict[str, str] = {}

    def load(self) -> None:
        settings_path = _CONFIG_DIR / "settings.yaml"
        profiles_path = _CONFIG_DIR / "default_profiles.json"

        if settings_path.exists():
            with open(settings_path, "r", encoding="utf-8") as fh:
                self._settings = yaml.safe_load(fh) or {}
        else:
            log.warning("settings.yaml missing, using empty defaults")

        if profiles_path.exists():
            with open(profiles_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                self._feature_defaults = data.get("features", {})
        else:
            log.warning("default_profiles.json missing, no feature defaults loaded")

        log.info("Config loaded: %d settings, %d feature defaults",
                  len(self._settings), len(self._feature_defaults))

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def get_feature_defaults(self) -> Dict[str, str]:
        return dict(self._feature_defaults)