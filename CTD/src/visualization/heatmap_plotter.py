"""
Heatmap Plotter for CTD data.
Converts profile dictionaries into 2D heatmaps.
"""

import os
from datetime import datetime
import pandas as pd
from data.time_series_2D import TimeSeries2D
from data.parameters import Parameter

class CTDHeatmapPlotter:
    """Handles transformation and rendering of CTD heatmaps."""
    
    def __init__(self, station="Default", parameter_name="Temperatura", 
                 top=0, depth=60, color_map=None, contour=True, measure_dots=False):
        self.station = station
        self.top = top
        self.depth = depth
        self.parameter = Parameter.get_by_name_es(parameter_name)
        if not self.parameter:
            # Fallback to basic parameter if not found
            self.parameter = Parameter(name=parameter_name, name_es=parameter_name, name_en=parameter_name)
        
        if color_map:
            self.parameter.color_map = color_map
        self.parameter.contour = contour
        self.parameter.measure_dots = measure_dots

    def plot(self, data_by_date, output_path):
        """
        Generates a heatmap from a dictionary of date strings and profile data.
        
        Args:
            data_by_date (dict): { "YYYY-MM-DDTHH:MM:SS": [ {var: val, Depth: val}, ... ] }
            output_path (str): File path to save the plot.
        """
        try:
            if not data_by_date:
                print("No data provided for heatmap.")
                return False
            
            clean_days, clean_vars, clean_depths = self._prepare_data(data_by_date)
            
            if not clean_days:
                print(f"No valid data found for parameter '{self.parameter.name_es}'")
                return False
            
            # Initialize engine
            engine = TimeSeries2D(clean_days, clean_vars, clean_depths)
            engine.station = self.station
            
            # Calculate range
            start_date = min(clean_days)
            end_date = max(clean_days)
            
            engine.plot(self.parameter, output_path,
                       top=self.top, depth=self.depth,
                       start=start_date, end=end_date)
            
            return True
        except Exception as e:
            print(f"Error generating heatmap: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _prepare_data(self, data_by_date):
        """Flattens dict into synchronized lists of Time, Value, and Depth."""
        clean_depths = []
        clean_vars = []
        clean_days = []
        
        # Searching for correctly named columns
        # The user's dataframe might have "Temperatura (ºC)" while Parameter says "Temperatura"
        
        for date_str, measurements in data_by_date.items():
            df = pd.DataFrame(measurements)
            
            # Find Depth column
            depth_col = "Profundidad" if "Profundidad" in df.columns else ("Presión" if "Presión" in df.columns else None)
            if not depth_col:
                continue
            
            # Find Parameter column (partial match)
            target = self.parameter.name_es
            var_col = next((c for c in df.columns if target.lower() in c.lower() and "_Flag" not in c), None)
            
            if not var_col:
                continue
            
            # Filter and drop NaNs
            sub_df = df.dropna(subset=[var_col, depth_col])
            if sub_df.empty:
                continue
            
            # Convert date
            try:
                # Handle full ISO format or just date
                dt = datetime.fromisoformat(date_str)
            except ValueError:
                dt = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
            
            clean_depths.extend(sub_df[depth_col].tolist())
            clean_vars.extend(sub_df[var_col].tolist())
            clean_days.extend([dt] * len(sub_df))
            
        return clean_days, clean_vars, clean_depths
