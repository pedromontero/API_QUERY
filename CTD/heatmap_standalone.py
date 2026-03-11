"""
Heatmap Standalone Generator for CTD_query.
Generates Depth vs. Time heatmaps for specific stations and parameters.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to python path to match پروژه pattern
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.ctd_client import CTDClient
from data.processor import DataProcessor
from visualization.heatmap_plotter import CTDHeatmapPlotter

def load_config(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def main():
    print("--- CTD_query: Heatmap Generator ---")
    
    # 1. Load configurations
    load_dotenv()
    common_cfg = load_config('input.json')
    heatmap_cfg = load_config('input_heatmap.json')
    
    if not common_cfg or not heatmap_cfg:
        print("Error: Missing input.json or input_heatmap.json")
        return

    # 2. Get API Credentials
    base_url = os.getenv("API_BASE_URL", "https://api.intecmar.gal")
    user = os.getenv("API_USER")
    password = os.getenv("API_PASSWORD")
    
    if not user or not password:
        print("Error: Credentials not found in .env")
        return

    # 3. Initialize API Client
    client = CTDClient(base_url, user, password)

    # 4. Processing parameters
    stations = common_cfg.get("stations", [])
    begin_date = common_cfg.get("begin_date")
    end_date = common_cfg.get("end_date")
    
    parameter_to_plot = heatmap_cfg.get("parameter", "Temperatura")
    output_dir = heatmap_cfg.get("output_dir", "plots/heatmaps")
    os.makedirs(output_dir, exist_ok=True)

    for station in stations:
        print(f"[*] Processing Station: {station}")
        
        # 1. Fetch raw data (including Depth/Pressure)
        variables = [parameter_to_plot, "Profundidad", "Presión"]
        raw_data = client.get_ctd_data(station, begin_date, end_date, variables)
        
        if not raw_data:
            print(f"    [!] No data found for station {station} in this period.")
            continue

        # 2. Process into domain models (Profiles)
        profiles = DataProcessor.process_raw_data(station, raw_data)
        
        if not profiles:
            print(f"    [!] No valid profiles found in response.")
            continue
            
        print(f"    [+] Found {len(profiles)} profiles for the heatmap.")
        
        # Accumulate data for the heatmap plotter
        station_data = {}
        for p in profiles:
            # Flatten measurements to dicts
            flat_data = []
            for m in p.measurements:
                row = {}
                if m.depth is not None: row["Profundidad"] = m.depth
                if m.pressure is not None: row["Presión"] = m.pressure
                row.update(m.values)
                flat_data.append(row)
            
            station_data[p.timestamp] = flat_data

        # Initialize Plotter
        plotter = CTDHeatmapPlotter(
            station=station,
            parameter_name=parameter_to_plot,
            top=heatmap_cfg.get("top", 0),
            depth=heatmap_cfg.get("depth", 60),
            color_map=heatmap_cfg.get("color_map"),
            contour=heatmap_cfg.get("contour", True),
            measure_dots=heatmap_cfg.get("measure_dots", True)
        )

        filename = f"heatmap_{station}_{parameter_to_plot.lower()}.png"
        output_path = os.path.join(output_dir, filename)
        
        if plotter.plot(station_data, output_path):
            print(f"    [OK] Heatmap generated: {output_path}")
        else:
            print(f"    [FAIL] Could not generate heatmap for {station}")

if __name__ == "__main__":
    main()
