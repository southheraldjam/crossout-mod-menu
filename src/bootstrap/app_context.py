"""
Application context wiring together services, handlers and adapters.
Keeps composition root logic out of main.py so it stays thin.
"""
from __future__ import annotations
import logging

from src.services.config_service import ConfigService
from src.services.process_service import ProcessService
from src.services.license_service import LicenseService
from src.services.update_service import UpdateService
from src.coremenu.menu_controller import MenuController
from src.overlay.overlay_handler import OverlayHandler
from src.handlers.hotkey_handler import HotkeyHandler
from src.adapters.windows_process_adapter import WindowsProcessAdapter

log = logging.getLogger("bootstrap.app_context")


class AppContext:
    def __init__(self, config_service: ConfigService, process_service: ProcessService,
                 license_service: LicenseService, update_service: UpdateService,
                 menu_controller: MenuController, overlay: OverlayHandler,
                 hotkeys: HotkeyHandler):
        self.config_service = config_service
        self.process_service = process_service
        self.license_service = license_service
        self.update_service = update_service
        self.menu_controller = menu_controller
        self.overlay = overlay
        self.hotkeys = hotkeys

    @classmethod
    def create(cls) -> "AppContext":
        config_service = ConfigService()
        config_service.load()

        adapter = WindowsProcessAdapter()
        process_service = ProcessService(adapter=adapter)
        license_service = LicenseService(config_service=config_service)
        update_service = UpdateService(config_service=config_service)

        menu_controller = MenuController(
            config_service=config_service,
            process_service=process_service,
        )
        overlay = OverlayHandler(menu_controller=menu_controller)
        hotkeys = HotkeyHandler(menu_controller=menu_controller)

        return cls(config_service, process_service, license_service,
                    update_service, menu_controller, overlay, hotkeys)

    def start(self) -> None:
        log.info("Validating license...")
        self.license_service.validate()

        log.info("Checking for updates...")
        self.update_service.check_for_update()

        log.info("Attaching to game process...")
        self.process_service.attach("Crossout.exe")

        self.hotkeys.register_defaults()
        self.overlay.show()
        self.overlay.run_loop()

    def shutdown(self) -> None:
        log.info("Detaching services and closing overlay")
        self.overlay.hide()
        self.process_service.detach()