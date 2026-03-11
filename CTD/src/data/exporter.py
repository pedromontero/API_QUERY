"""
Author: Pedro Montero
Organization: INTECMAR
License: Open Source
"""

import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

class ExcelExporter:
    """
    Handles exporting CTD data to Excel files.
    """
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def export_station_data(self, station_code, profiles_data):
        """
        Exports multiple profiles for a single station into one Excel file.
        Each profile goes into a separate sheet named YYYYMMDD.
        profiles_data: List of dicts, each with 'date', 'time', and 'data' (list of dicts)
        """
        file_path = os.path.join(self.output_dir, f"CTD_{station_code}.xlsx")
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for profile in profiles_data:
                date_str = profile['date'] # Expected YYYY-MM-DD
                sheet_name = date_str.replace('-', '')
                time_str = profile.get('time', '00:00:00')
                
                df = pd.DataFrame(profile['data'])
                
                # Ensure Depth and Pressure are first (if they exist)
                cols = list(df.columns)
                fixed_cols = []
                for p in ["Profundidad", "Presión"]:
                    if p in cols:
                        fixed_cols.append(p)
                        cols.remove(p)
                
                final_cols = fixed_cols + cols
                df = df[final_cols]
                
                # Write to sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)
                
                # Add custom header
                workbook = writer.book
                worksheet = workbook[sheet_name]
                worksheet['A1'] = f"Station: {station_code}"
                worksheet['A2'] = f"Date: {date_str} Time: {time_str}"
                
                # We could add units here if the API provides them, 
                # but based on docs it's usually just variable names.
                # If variables are like "Temperatura (ºC)", they are already in columns.
