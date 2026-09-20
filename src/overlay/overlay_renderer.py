"""
Rendering shim for the in-game overlay window. In this build the
actual DirectX/OpenGL hook is delegated to native adapters; this
module only manages the logical draw state used by tests and UI mocks.
"""
from __future__ import annotations
import logging
from typing import Dict

log = logging.getLogger("overlay.overlay_renderer")


class OverlayRenderer:
    def __init__(self):
        self._window_open = False
        self._last_frame: Dict[str, bool] = {}

    def create_window(self, title: str) -> None:
        self._window_open = True
        log.debug("Renderer window '%s' opened", title)

    def destroy_window(self) -> None:
        self._window_open = False
        log.debug("Renderer window closed")

    def draw_frame(self, features: Dict[str, bool]) -> None:
        if not self._window_open:
            return
        self._last_frame = dict(features)

    def get_last_frame(self) -> Dict[str, bool]:
        return self._last_frame