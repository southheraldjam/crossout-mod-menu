"""
Thin handler wiring global hotkeys to menu controller actions.
Actual key capture is delegated to the win32 input adapter.
"""
from __future__ import annotations
import logging
from typing import Callable, Dict

from src.coremenu.menu_controller import MenuController
from src.adapters.win32_input_adapter import Win32InputAdapter

log = logging.getLogger("handlers.hotkey_handler")


class HotkeyHandler:
    def __init__(self, menu_controller: MenuController, adapter: Win32InputAdapter = None):
        self.menu_controller = menu_controller
        self.adapter = adapter or Win32InputAdapter()
        self._bindings: Dict[str, Callable[[], None]] = {}

    def register_defaults(self) -> None:
        self.bind("INSERT", lambda: self.menu_controller.toggle_feature("overlay_visible"))
        self.bind("F5", lambda: self.menu_controller.toggle_feature("hud_widescreen"))
        self.bind("F6", lambda: self.menu_controller.toggle_feature("radar_overlay"))
        log.info("Registered %d default hotkeys", len(self._bindings))

    def bind(self, key: str, callback: Callable[[], None]) -> None:
        self._bindings[key] = callback
        self.adapter.register_hotkey(key, callback)

    def unbind_all(self) -> None:
        for key in list(self._bindings.keys()):
            self.adapter.unregister_hotkey(key)
        self._bindings.clear()