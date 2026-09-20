"""
Business service for managing the lifecycle of the connection to
the target game process. Delegates OS-level work to the platform
adapter interface.
"""
from __future__ import annotations
import logging
from typing import Optional

from src.adapters.windows_process_adapter import WindowsProcessAdapter

log = logging.getLogger("services.process_service")


class ProcessAttachError(Exception):
    pass


class ProcessService:
    def __init__(self, adapter: WindowsProcessAdapter):
        self.adapter = adapter
        self._attached_pid: Optional[int] = None

    def attach(self, process_name: str) -> int:
        pid = self.adapter.find_process_id(process_name)
        if pid is None:
            raise ProcessAttachError(f"Process '{process_name}' not found")

        handle_ok = self.adapter.open_handle(pid)
        if not handle_ok:
            raise ProcessAttachError(f"Unable to open handle for pid {pid}")

        self._attached_pid = pid
        log.info("Attached to process '%s' (pid=%d)", process_name, pid)
        return pid

    def detach(self) -> None:
        if self._attached_pid is not None:
            self.adapter.close_handle(self._attached_pid)
            log.info("Closed handle for pid=%d", self._attached_pid)
        self._attached_pid = None

    def is_attached(self) -> bool:
        return self._attached_pid is not None