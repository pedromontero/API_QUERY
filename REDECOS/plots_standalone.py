"""
Standalone script to generate REDECOS Time Series plots.
Author: Pedro Montero
Organization: INTECMAR
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.redecos_client import RedecosClient
from data.redecos_processor import RedecosDataProcessor
from visualization.redecos_plotter import RedecosPlotter

def load_config():
    """Merges common and specific plot config."""
    common = {}
    if os.path.exists("input.json"):
        with open("input.json", 'r', encoding='utf-8') as f:
            common = json.load(f)
            
    specific = {}
    if os.path.exists("input_plots.json"):
        with open("input_plots.json", 'r', encoding='utf-8') as f:
            specific = json.load(f)
            
    return {**common, **specific}

def main():
    print("--- Redecos: Plotting Standalone ---")
    
    # Environment
    if os.path.exists(".env"):
        load_dotenv(".env")
    else:
        load_dotenv("../MOORINGS/.env") # fallback common
        
    config = load_config()
    
    # Inputs
    begin_date = config.get("begin_date", "2023-01-01")
    end_date = config.get("end_date", "2023-01-15")
    stations = config.get("stations", [])
    variables = config.get("variables", [])
    plots_dir = config.get("plots_dir", "plots")
    
    # Client
    client = RedecosClient(
        os.getenv("API_BASE_URL", "https://api.intecmar.gal"),
        os.getenv("API_USER"),
        os.getenv("API_PASSWORD")
    )
    
    # Metadata for resolution
    try:
        stations_meta = client.get_stations()
        params_meta = client.get_parameters()
    except Exception as e:
        print(f"[ERR] Failed to fetch metadata: {e}")
        return

    processor = RedecosDataProcessor(stations_meta, params_meta)
    plotter = RedecosPlotter(plots_dir)
    
    # Process each station
    for s_code in stations:
        # Find station name
        s_name = next((s["StationName"] for s in stations_meta if s["StationCode"] == s_code), s_code)
        print(f"[*] Processing Plots for Station: {s_name} ({s_code})")
        
        for var in variables:
            try:
                # 1. Fetch raw data
                json_data = client.get_station_data(s_code, var, begin_date, end_date)
                
                # 2. Convert to batch
                batch = processor.process_data(json_data, s_code, var)
                
                if batch and batch.measurements:
                    # 3. Plot
                    path = plotter.plot_time_series(batch, station_name=s_name)
                    if path:
                        print(f"    [OK] Generated plot for {batch.parameter_name}")
                else:
                    print(f"    [SKIP] No valid data for {var} in this range.")
                    
            except Exception as e:
                print(f"    [ERR] Plotting {var}: {e}")

if __name__ == "__main__":
    main()
