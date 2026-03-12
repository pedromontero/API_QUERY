"""
Data processor for REDECOS network.
Author: Pedro Montero
Organization: INTECMAR
"""

from datetime import datetime
from typing import List
from models.domain import RedecosBatch, RedecosMeasurement

class RedecosDataProcessor:
    """
    Handles translation from API JSON to structured domain models.
    """
    def __init__(self, stations_metadata=None, params_metadata=None):
        self.stations_metadata = stations_metadata or []
        self.params_metadata = params_metadata or []

    def get_parameter_info(self, param_id_or_name: str):
        """Resolves units and correct name from metadata."""
        for p in self.params_metadata:
            if str(p.get("Id")) == str(param_id_or_name) or p.get("Name") == param_id_or_name:
                return p.get("Name"), p.get("Units", "-"), p.get("Id")
        return param_id_or_name, "-", param_id_or_name

    def process_data(self, json_data, station_code, parameter_id_or_name):
        """
        Converts a list of measurements from API into a RedecosBatch.
        """
        if not json_data:
            return None
            
        param_name, units, param_id = self.get_parameter_info(parameter_id_or_name)
        
        batch = RedecosBatch(
            station_code=station_code,
            parameter_id=param_id,
            parameter_name=param_name,
            units=units,
            measurements=[]
        )
        
        # The API returns either a list or a dict with a "Data" key
        measurements_list = []
        if isinstance(json_data, dict):
            measurements_list = json_data.get("Data", [])
        elif isinstance(json_data, list):
            measurements_list = json_data
            
        if not isinstance(measurements_list, list):
            return batch
            
        for item in measurements_list:
            if not isinstance(item, dict):
                continue
            ts = item.get("DateTime")
            val = item.get("Value")
            val_code = item.get("ValidationCode", 1)
            val_level = item.get("ValidationLevel", 1)
            
            if val is None:
                continue
                
            try:
                # API format: 2026-01-01T10:00:00
                dt_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                continue
                
            measurement = RedecosMeasurement(
                timestamp=ts,
                date_obj=dt_obj,
                value=float(val),
                flag=int(val_code),
                validation_level=int(val_level)
            )
            batch.measurements.append(measurement)
            
        return batch
