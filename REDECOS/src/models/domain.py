from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class RedecosMeasurement:
    timestamp: str
    date_obj: datetime
    value: float
    flag: int
    validation_level: int = 1

@dataclass
class RedecosBatch:
    station_code: str
    parameter_id: Optional[str]
    parameter_name: str
    units: str
    measurements: List[RedecosMeasurement] = field(default_factory=list)
