from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class MooringMeasurement:
    timestamp: str
    date_obj: datetime
    value: float
    flag: int
    depth: Optional[float] = None # Added for multi-depth cases

@dataclass
class MooringBatch:
    station_code: str
    parameter_id: int
    parameter_name: str
    units: str
    frequency: str
    measurements: List[MooringMeasurement] = field(default_factory=list)
