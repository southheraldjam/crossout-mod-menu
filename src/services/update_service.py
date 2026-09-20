"""
Service that checks the configured update endpoint for newer
mod-menu builds and reports the result to the log/UI.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass

from src.services.config_service import ConfigService

log = logging.getLogger("services.update_service")


@dataclass
class UpdateInfo:
    current_version: str
    latest_version: str
    update_available: bool


class UpdateService:
    CURRENT_VERSION = "2026.1.0"

    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def check_for_update(self) -> UpdateInfo:
        endpoint = self.config_service.get("update_endpoint", "https://updates.local/crossout-mod-menu")
        log.debug("Checking update endpoint: %