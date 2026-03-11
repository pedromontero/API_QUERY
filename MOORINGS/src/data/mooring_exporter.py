"""
Excel Exporter for Mooring data.
Converts batches into a structured Excel file per station.
"""

import os
import pandas as pd

class MooringExporter:
    """
    Handles exporting Mooring batches to Excel files.
    """
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_station_excel(self, batches, station_code, station_name="Station"):
        """
        Combines batches (different parameters/depths) into a single Excel sheet.
        """
        if not batches:
            return None

        # Build a master dataframe indexed by Time
        # Since different depths might have samples at the same time,
        # we index by (Time, Depth) or create separate columns.
        # Most users prefer columns: [Time, Temp_1m, Temp_1m_Flag, Temp_3m, Temp_3m_Flag, ...]
        
        master_df = None
        
        for batch in batches:
            param = batch.parameter_name
            depth = batch.measurements[0].depth
            freq = batch.frequency
            
            # Create unique header name
            depth_suffix = f"_{depth}m" if depth is not None else ""
            val_col = f"{param}{depth_suffix}"
            flag_col = f"{param}{depth_suffix}_Flag"
            
            data = []
            for m in batch.measurements:
                data.append({
                    "Date (UTC)": m.timestamp,
                    val_col: m.value,
                    flag_col: m.flag
                })
            
            df = pd.DataFrame(data)
            if df.empty:
                continue
            df.set_index("Date (UTC)", inplace=True)
            
            if master_df is None:
                master_df = df
            else:
                # Outer join to combine all times across parameters
                master_df = master_df.join(df, how="outer")

        if master_df is None or master_df.empty:
            return None

        # Sort by date
        master_df.index = pd.to_datetime(master_df.index)
        # Strip timezone for Excel compatibility
        if master_df.index.tz is not None:
            master_df.index = master_df.index.tz_localize(None)
        master_df.sort_index(inplace=True)

        filename = f"mooring_{station_code}_{station_name.lower().replace(' ', '_')}.xlsx"
        output_path = os.path.join(self.output_dir, filename)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            master_df.to_excel(writer, sheet_name="Mooring Data")
            # Auto-adjust columns width (simplified)
            worksheet = writer.sheets['Mooring Data']
            for i, col in enumerate(master_df.columns):
                column_len = max(master_df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(66 + i)].width = column_len

        return output_path
