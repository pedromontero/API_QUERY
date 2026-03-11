"""
Standalone script to export Mooring data to Excel.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.mooring_client import MooringClient
from data.mooring_processor import MooringDataProcessor
from data.mooring_exporter import MooringExporter

def load_merged_config():
    config = {}
    # Load common
    if os.path.exists('input.json'):
        with open('input.json', 'r', encoding='utf-8') as f:
            config.update(json.load(f))
    # Load specific
    if os.path.exists('input_export.json'):
        with open('input_export.json', 'r', encoding='utf-8') as f:
            config.update(json.load(f))
    return config

def main():
    print("--- Mooring: Excel Export Standalone ---")
    load_dotenv()
    config = load_merged_config()
    
    if not config:
        print("Error: Configuration files not found.")
        return

    client = MooringClient(os.getenv("API_BASE_URL"), os.getenv("API_USER"), os.getenv("API_PASSWORD"))
    processor = MooringDataProcessor()
    exporter = MooringExporter(output_dir=config.get("output_dir", "output"))

    stations = config.get("stations", [])
    begin_date = config.get("begin_date")
    end_date = config.get("end_date")
    variables = config.get("variables", [])
    frequency = config.get("frequency", "daily")
    func = config.get("function", "AVG")

    all_stations = client.get_stations()
    station_map = {s['StationCode']: s['StationName'] for s in all_stations}

    for station_code in stations:
        name = station_map.get(station_code, station_code)
        print(f"[*] Processing Excel for: {name}")
        
        available_params = client.get_station_parameters(station_code)
        param_map = {}
        for p in available_params:
            param_map[str(p.get("ParameterCode")).lower()] = str(p.get("ParameterCode"))
            param_map[str(p.get("ParameterName")).lower()] = str(p.get("ParameterCode"))
            param_map[str(p.get("Description", "")).lower()] = str(p.get("ParameterCode"))

        all_station_batches = []
        for var in variables:
            p_id = param_map.get(var.lower())
            if not p_id: continue
            
            try:
                raw = client.get_mooring_data(station_code, p_id, frequency, begin_date, end_date, function=func)
                batches = processor.process_raw_data(raw)
                if batches:
                    all_station_batches.extend(batches)
            except Exception as e:
                print(f"    [ERR] Fetching {var} for Excel: {e}")

        if all_station_batches:
            path = exporter.export_station_excel(all_station_batches, station_code, station_name=name)
            if path:
                print(f"    [OK] Generated Excel: {os.path.basename(path)}")

if __name__ == "__main__":
    main()
