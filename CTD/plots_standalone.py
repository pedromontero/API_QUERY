import os
import json
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from api.ctd_client import CTDClient
from data.processor import DataProcessor
from visualization.plotter import ProfilePlotter

def main():
    load_dotenv()
    
    # Load configs
    with open('input.json', 'r', encoding='utf-8') as f:
        common = json.load(f)
    with open('input_plots.json', 'r', encoding='utf-8') as f:
        plots_cfg = json.load(f)

    api_url = os.getenv("API_BASE_URL", "https://api.intecmar.gal")
    client = CTDClient(api_url, os.getenv("API_USER"), os.getenv("API_PASSWORD"))
    plotter = ProfilePlotter(plots_cfg.get("plots_dir", "plots"))

    print("--- Standalone Plotting ---")
    for station in common.get("stations", []):
        print(f"[*] Plotting Station: {station}")
        raw_data = client.get_ctd_data(station, common["begin_date"], common["end_date"], common["variables"])
        if not raw_data: continue
        
        profiles = DataProcessor.process_raw_data(station, raw_data)
        for profile in profiles:
            flat_data = []
            for m in profile.measurements:
                row = {"Profundidad": m.depth, "Presión": m.pressure}
                row.update(m.values)
                flat_data.append(row)
            
            plotter.plot_profile(
                station, 
                profile.date_str, 
                flat_data, 
                time_str=profile.time_str,
                only_good_data=plots_cfg.get("only_good_data", False),
                scaled_plots=plots_cfg.get("scaled_plots", False),
                custom_scales=plots_cfg.get("custom_scales", {})
            )

if __name__ == "__main__":
    main()
