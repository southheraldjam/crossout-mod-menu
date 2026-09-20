"""
Handler responsible for coordinating attach/detach lifecycle events
between the process service and UI layer. Kept intentionally thin;
all platform-specific work lives in adapters.
"""
from __future__ import annotations
import logging

from src.services.process_service import ProcessService, ProcessAttachError

log = logging.getLogger("handlers.injection_handler")


class InjectionHandler:
    def __init__(self, process_service: ProcessService):
        self.process_service = process_service

    def try_attach(self, process_name: str) -> bool:
        try:
            self.process_service.attach(process_name)
            log.info("Attached to '%s' successfully", process_name)
            return True
        except ProcessAttachError as exc:
            log.error("Attach failed: %s", exc)
            return False

    def detach(self) -> None:
        self.process_service.detach()
        log.info("Detached from target process")