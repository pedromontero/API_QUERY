import os
import json
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from api.ctd_client import CTDClient
from data.processor import DataProcessor
from data.exporter import ExcelExporter

def main():
    load_dotenv()
    
    # Load configs
    with open('input.json', 'r', encoding='utf-8') as f:
        common = json.load(f)
    with open('input_export.json', 'r', encoding='utf-8') as f:
        export_cfg = json.load(f)

    api_url = os.getenv("API_BASE_URL", "https://api.intecmar.gal")
    client = CTDClient(api_url, os.getenv("API_USER"), os.getenv("API_PASSWORD"))
    exporter = ExcelExporter(export_cfg.get("output_dir", "output"))

    print("--- Standalone Excel Export ---")
    for station in common.get("stations", []):
        print(f"[*] Exporting Station: {station}")
        raw_data = client.get_ctd_data(station, common["begin_date"], common["end_date"], common["variables"])
        if not raw_data: continue
        
        profiles = DataProcessor.process_raw_data(station, raw_data)
        export_profiles = []
        for profile in profiles:
            flat_data = []
            for m in profile.measurements:
                row = {"Profundidad": m.depth, "Presión": m.pressure}
                row.update(m.values)
                flat_data.append(row)
            export_profiles.append({'date': profile.date_str, 'time': profile.time_str, 'data': flat_data})
        
        exporter.export_station_data(station, export_profiles)

if __name__ == "__main__":
    main()
