"""
Crossout Mod Menu - Entry point
Bootstraps the application context, loads configuration and starts
the overlay + hotkey listeners.
"""
import sys
import logging

from src.bootstrap.app_context import AppContext
from src.utils.logger import configure_logging


def main() -> int:
    configure_logging()
    log = logging.getLogger("bootstrap.main")
    log.info("Starting Crossout Mod Menu (build 2026.1)")

    ctx = AppContext.create()
    try:
        ctx.start()
    except KeyboardInterrupt:
        log.info("Shutdown requested by user")
    except Exception:
        log.exception("Fatal error during runtime, shutting down")
        return 1
    finally:
        ctx.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())