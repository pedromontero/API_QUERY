"""
Mooring Plotter for Time Series.
Generates professional plots with multiple depths and quality indicators.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from datetime import datetime

class MooringPlotter:
    """
    Handles plotting of Mooring time series data.
    """
    
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set_theme(style="whitegrid")

    def plot_time_series(self, batches, station_name=None):
        """
        Plots one or more batches (typically same parameter at different depths).
        """
        if not batches:
            return None
            
        first = batches[0]
        param_name = first.parameter_name
        station_code = first.station_code
        units = first.units
        
        plt.figure(figsize=(12, 6))
        
        # Color palette for depths
        palette = sns.color_palette("husl", len(batches))
        
        for i, batch in enumerate(batches):
            # FILTER: QualityCode distinct from 9
            valid_m = [m for m in batch.measurements if m.flag != 9]
            
            df = pd.DataFrame([
                {
                    "date": m.date_obj,
                    "value": m.value,
                    "flag": m.flag
                } for m in valid_m
            ])
            
            if df.empty:
                continue
                
            label = f"{param_name}"
            if batch.measurements[0].depth is not None:
                label += f" ({batch.measurements[0].depth}m)"
            
            # Plot line
            sns.lineplot(data=df, x="date", y="value", label=label, color=palette[i], linewidth=1.5, alpha=0.8)
            
            # Plot quality indicators (optional, maybe just for Flag 4?)
            bad_data = df[df["flag"] == 4]
            if not bad_data.empty:
                plt.scatter(bad_data["date"], bad_data["value"], color="black", marker="x", s=30, label="Flag 4 (Bad)" if i == 0 else "")

        title = f"{station_name or station_code} - {param_name}"
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel(f"{param_name} ({units})", fontsize=12)
        
        # Format X axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)
        
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        filename = f"timeseries_{station_code}_{param_name.lower().replace(' ', '_')}.png"
        save_path = os.path.join(self.output_dir, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()
        
        return save_path
