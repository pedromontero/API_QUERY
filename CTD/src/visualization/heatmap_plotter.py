# -*- coding: utf-8 -*-

#    !------------------------------------------------------------------------------
#    !                       OCXG API, CAPTA Project
#    !------------------------------------------------------------------------------
#    !
#    ! TITLE         : OCXG API_QUERY
#    ! PROJECT       : CAPTA
#    ! URL           : http://observatoriocosteiro.gal/es
#    ! AFFILIATION   : INTECMAR
#    ! DATE          : March 2026
#    ! REVISION      : Montero 0.1
#    !> @author
#    !> Pedro Montero Vilar
#    !
#    ! DESCRIPTION:
#    ! Preprocessing script for collecting data from OCXG API and processing them
#    !--------------------------------------------------------------------------------------
#
#    MIT License
#
#    Copyright (c) 2026 INTECMAR
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

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
        
        for date_str, measurements in data_by_date.items():
            df = pd.DataFrame(measurements)
            
            # Find Depth column (case-insensitive)
            depth_col = next((c for c in df.columns if "profundidad" in c.lower() or "presi" in c.lower()), None)
            if not depth_col:
                continue
            
            # Find Parameter column (case-insensitive and excluding flags)
            target = self.parameter.name_es.lower()
            var_col = next((c for c in df.columns if target in c.lower() and "_flag" not in c.lower()), None)
            
            if not var_col:
                continue
            
            # Find corresponding Flag column
            clean_var_no_units = var_col.split(' (')[0]
            flag_col = next((c for c in df.columns if c.startswith(clean_var_no_units) and c.endswith("_Flag")), None)
            
            # Filter: drop NaNs in coordinates or variable
            subset = [var_col, depth_col]
            if flag_col:
                subset.append(flag_col)
                
            sub_df = df.dropna(subset=[var_col, depth_col])
            
            # FILTER: Exclude Flag 4 (Bad Data)
            if flag_col:
                sub_df = sub_df[sub_df[flag_col] != 4]
            
            if sub_df.empty:
                continue
            
            # Convert date
            try:
                dt = datetime.fromisoformat(date_str)
            except ValueError:
                dt = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
            
            clean_depths.extend(sub_df[depth_col].tolist())
            clean_vars.extend(sub_df[var_col].tolist())
            clean_days.extend([dt] * len(sub_df))
            
        return clean_days, clean_vars, clean_depths
