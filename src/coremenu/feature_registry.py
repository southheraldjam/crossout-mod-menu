"""
Registry that maps configurable mod-menu feature keys to their
in-memory toggle state, driven by the loaded profile config.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

from src.services.config_service import ConfigService

log = logging.getLogger("coremenu.feature_registry")


@dataclass
class MenuFeature:
    key: str
    display_name: str
    enabled: bool = False

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled

    def disable(self) -> None:
        self.enabled = False


class FeatureRegistry:
    def __init__(self, config_service: ConfigService):
        self._features: Dict[str, MenuFeature] = {}
        self._load(config_service)

    def _load(self, config_service: ConfigService) -> None:
        defaults = config_service.get_feature_defaults()
        for key, display_name in defaults.items():
            self._features[key] = MenuFeature(key=key, display_name=display_name)
        log.debug("Loaded %d features into registry", len(self._features))

    def get(self, key: str) -> Optional[MenuFeature]:
        return self._features.get(key)

    def all(self) -> Dict[str, MenuFeature]:
        return self._features