"""
Author: Pedro Montero
Organization: INTECMAR
License: Open Source
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Measurement:
    """Represents a single point in a CTD profile."""
    depth: float = None
    pressure: float = None
    values: Dict[str, Any] = field(default_factory=dict)
    flags: Dict[str, int] = field(default_factory=dict)

@dataclass
class CTDProfile:
    """Represents a full CTD profile for a station at a specific time."""
    station_code: str
    timestamp: str
    measurements: List[Measurement] = field(default_factory=list)

    @property
    def date_str(self) -> str:
        return self.timestamp[:10]

    @property
    def time_str(self) -> str:
        return self.timestamp[11:19]
