"""
Plotting module for REDECOS (Coastal Observation Network) data.
Author: Pedro Montero
Organization: INTECMAR
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from models.domain import RedecosBatch

class RedecosPlotter:
    """
    Generates time-series plots for REDECOS parameters.
    """
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set_theme(style="whitegrid")

    def plot_time_series(self, batch: RedecosBatch, station_name=None):
        """
        Plots a batch of data for a single parameter.
        """
        if not batch or not batch.measurements:
            return None
            
        param_name = batch.parameter_name
        station_code = batch.station_code
        units = batch.units
        
        plt.figure(figsize=(12, 6))
        
        # Valid data filtering (exclude flag 9 as per Mooring philosophy)
        valid_m = [m for m in batch.measurements if m.flag != 9]
        
        df = pd.DataFrame([
            {
                "date": m.date_obj,
                "value": m.value,
                "flag": m.flag
            } for m in valid_m
        ])
        
        if df.empty:
            return None

        # Plot line
        sns.lineplot(data=df, x="date", y="value", label=param_name, color="#0077b6", linewidth=1.5, alpha=0.8)

        title = f"{station_name or station_code} - {param_name}"
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.xlabel("Date (UTC)", fontsize=12)
        plt.ylabel(f"{param_name} ({units})", fontsize=12)
        
        # Format X axis for dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)
        
        plt.legend()
        plt.tight_layout()
        
        filename = f"timeseries_{station_code}_{param_name.lower().replace(' ', '_')}.png"
        save_path = os.path.join(self.output_dir, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()
        
        return save_path
