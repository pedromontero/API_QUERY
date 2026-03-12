"""
Standalone script to export REDECOS data to Excel.
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
from data.redecos_exporter import RedecosExporter

def load_config():
    """Merges common and specific export config."""
    common = {}
    if os.path.exists("input.json"):
        with open("input.json", 'r', encoding='utf-8') as f:
            common = json.load(f)
            
    specific = {}
    if os.path.exists("input_export.json"):
        with open("input_export.json", 'r', encoding='utf-8') as f:
            specific = json.load(f)
            
    return {**common, **specific}

def main():
    print("--- Redecos: Excel Export Standalone ---")
    
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
    output_dir = config.get("output_dir", "output")
    
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
    exporter = RedecosExporter(output_dir)
    
    # Process each station
    for s_code in stations:
        # Find station name
        s_name = next((s["StationName"] for s in stations_meta if s["StationCode"] == s_code), s_code)
        
        station_batches = []
        print(f"[*] Exporting Station: {s_name} ({s_code})")
        
        for var in variables:
            try:
                # 1. Fetch raw data
                json_data = client.get_station_data(s_code, var, begin_date, end_date)
                
                # 2. Convert to batch
                batch = processor.process_data(json_data, s_code, var)
                
                if batch and batch.measurements:
                    station_batches.append(batch)
                    
            except Exception as e:
                print(f"    [ERR] Fetching {var}: {e}")

        if station_batches:
            # 3. Export all variables for this station to one file
            path = exporter.export_station_excel(station_batches, s_code, station_name=s_name)
            if path:
                print(f"    [OK] Generated Excel: {os.path.basename(path)}")
        else:
            print(f"    [SKIP] No data found for requested variables in this range.")

if __name__ == "__main__":
    main()
