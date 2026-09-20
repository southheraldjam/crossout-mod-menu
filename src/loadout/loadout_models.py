"""
Data models for loadout profiles used across the mod menu UI and
persistence layer.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class LoadoutProfile:
    name: str
    hud_scale: float = 1.0
    hotkey_map: Dict[str, str] = field(default_factory=dict)
    enabled_features: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "hud_scale": self.hud_scale,
            "hotkey_map": self.hotkey_map,
            "enabled_features": self.enabled_features,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoadoutProfile":
        return cls(
            name=data["name"],
            hud_scale=data.get("hud_scale", 1.0),
            hotkey_map=data.get("hotkey_map", {}),
            enabled_features=data.get("enabled_features", {}),
        )