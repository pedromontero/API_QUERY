"""
Data Processor for Mooring data.
Converts raw API responses into domain models.
"""

from datetime import datetime
from models.domain import MooringMeasurement, MooringBatch

class MooringDataProcessor:
    """
    Processes raw Mooring data into high-level batches.
    """
    
    @staticmethod
    def process_raw_data(raw_data):
        """
        Parses the list of objects returned by the Mooring data endpoint.
        
        Args:
            raw_data (list): List of objects (one per depth/configuration).
            
        Returns:
            list[MooringBatch]: List of processed batches.
        """
        batches = []
        if not raw_data or not isinstance(raw_data, list):
            return batches
            
        for entry in raw_data:
            metadata = entry
            samples = entry.get("Samples", [])
            
            if not samples:
                continue
                
            batch = MooringBatch(
                station_code=str(metadata.get("StationCode")),
                parameter_id=metadata.get("ParameterId"),
                parameter_name=metadata.get("ParameterCode", "Unknown"),
                units=metadata.get("Units", ""),
                frequency=metadata.get("Frequency", "unknown"),
                measurements=[]
            )
            
            depth = metadata.get("Depth")
            
            for s in samples:
                raw_date = s.get("Date")
                try:
                    # '2023-01-31T00:00:00Z'
                    dt = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                except:
                    dt = datetime.strptime(raw_date.split('T')[0], "%Y-%m-%d")
                    
                meas = MooringMeasurement(
                    timestamp=raw_date,
                    date_obj=dt,
                    value=float(s.get("Value", 0.0)),
                    flag=int(s.get("QualityCode", 0)),
                    depth=depth
                )
                batch.measurements.append(meas)
                
            # Sort measurements by date
            batch.measurements.sort(key=lambda x: x.date_obj)
            batches.append(batch)
            
        return batches
