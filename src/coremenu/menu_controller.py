"""
Core controller for the mod menu feature set.
Thin coordination layer between overlay UI, hotkeys and business services.
"""
from __future__ import annotations
import logging
from typing import Dict

from src.coremenu.feature_registry import FeatureRegistry
from src.services.config_service import ConfigService
from src.services.process_service import ProcessService
from src.models.session_state import SessionState

log = logging.getLogger("coremenu.menu_controller")


class MenuController:
    def __init__(self, config_service: ConfigService, process_service: ProcessService):
        self.config_service = config_service
        self.process_service = process_service
        self.registry = FeatureRegistry(config_service=config_service)
        self.session = SessionState()

    def toggle_feature(self, feature_key: str) -> bool:
        if not self.process_service.is_attached():
            log.warning("Cannot toggle '%s', process not attached", feature_key)
            return False

        feature = self.registry.get(feature_key)
        if feature is None:
            log.warning("Unknown feature key: %s", feature_key)
            return False

        new_state = feature.toggle()
        self.session.record_toggle(feature_key, new_state)
        log.info("Feature '%s' set to %s", feature_key, new_state)
        return new_state

    def get_visible_features(self) -> Dict[str, bool]:
        return {key: feat.enabled for key, feat in self.registry.all().items()}

    def reset_session(self) -> None:
        self.session = SessionState()
        for feature in self.registry.all().values():
            feature.disable()