"""
Business logic for managing user loadout/profile presets used by
the mod menu (weapon layout labels, HUD tweaks, saved hotkey sets).
"""
from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import List, Optional

from src.loadout.loadout_models import LoadoutProfile
from src.utils.paths import get_config_dir

log = logging.getLogger("loadout.loadout_service")


class LoadoutService:
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or (get_config_dir() / "loadout_profiles.json")
        self._profiles: List[LoadoutProfile] = []
        self._loaded = False

    def load_all(self) -> List[LoadoutProfile]:
        if not self.storage_path.exists():
            log.info("No loadout file found at %s, starting empty", self.storage_path)
            self._profiles = []
            self._loaded = True
            return self._profiles

        with open(self.storage_path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)

        self._profiles = [LoadoutProfile.from_dict(item) for item in raw]
        self._loaded = True
        return self._profiles

    def save_profile(self, profile: LoadoutProfile) -> None:
        if not self._loaded:
            self.load_all()

        existing = next((p for p in self._profiles if p.name == profile.name), None)
        if existing:
            self._profiles.remove(existing)
        self._profiles.append(profile)
        self._persist()

    def delete_profile(self, name: str) -> bool:
        if not self._loaded:
            self.load_all()

        before = len(self._profiles)
        self._profiles = [p for p in self._profiles if p.name != name]
        if len(self._profiles) != before:
            self._persist()
            return True
        return False

    def _persist(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as fh:
            json.dump([p.to_dict() for p in self._profiles], fh, indent=2)
        log.debug("Persisted %d loadout profiles", len(self._profiles))