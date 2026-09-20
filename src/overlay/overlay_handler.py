"""
Thin handler responsible for showing/hiding the mod menu overlay
window and dispatching UI events into the menu controller.
"""
from __future__ import annotations
import logging
import time

from src.coremenu.menu_controller import MenuController
from src.overlay.overlay_renderer import OverlayRenderer

log = logging.getLogger("overlay.overlay_handler")


class OverlayHandler:
    def __init__(self, menu_controller: MenuController):
        self.menu_controller = menu_controller
        self.renderer = OverlayRenderer()
        self._visible = False
        self._running = False

    def show(self) -> None:
        self._visible = True
        self.renderer.create_window(title="Crossout Mod Menu")
        log.info("Overlay window created")

    def hide(self) -> None:
        self._visible = False
        self._running = False
        self.renderer.destroy_window()
        log.info("Overlay window destroyed")

    def run_loop(self) -> None:
        self._running = True
        log.info("Entering overlay render loop")
        while self._running and self._visible:
            features = self.menu_controller.get_visible_features()
            self.renderer.draw_frame(features)
            time.sleep(0.016)  # ~60fps tick, placeholder for real event pump

    def stop(self) -> None:
        self._running = False