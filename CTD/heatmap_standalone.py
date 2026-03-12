# -*- coding: utf-8 -*-

"""
!==============================================================================!
!                OCXG API - CAPTA PROJECT (INTECMAR)                           !
!==============================================================================!
!                                                                              !
! TITLE        : OCXG API_QUERY                                                !
! PROJECT      : CAPTA (Coastal Observatory of Galicia)                        !
! URL          : http://observatoriocosteiro.gal/es                            !
! AFFILIATION  : INTECMAR (Xunta de Galicia)                                   !
!                                                                              !
! DATE         : March 2026                                                    !
! VERSION      : 0.1.0-alpha                                                   !
! REVISION     : Montero 0.1                                                   !
!                                                                              !
! AUTHOR       : Pedro Montero Vilar                                           !
! CONTACT      : pmontero@intecmar.gal                                         !
!                                                                              !
! DESCRIPTION  : Standalone script for Heatmap.                                !
!                                                                              !
!==============================================================================!
!                               MIT LICENSE                                    !
!------------------------------------------------------------------------------!
! Copyright (c) 2026 INTECMAR                                                  !
!                                                                              !
! Permission is hereby granted, free of charge, to any person obtaining a copy  !
! of this software and associated documentation files (the "Software"), to deal !
! in the Software without restriction, including without limitation the rights  !
! to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    !
! copies of the Software, and to permit persons to whom the Software is        !
! furnished to do so, subject to the following conditions:                     !
!                                                                              !
! The above copyright notice and this permission notice shall be included in   !
! all copies or substantial portions of the Software.                          !
!                                                                              !
! THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   !
! IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      !
! FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  !
! AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       !
! LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, !
! OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN    !
! THE SOFTWARE.                                                                !
!==============================================================================!
"""

__author__      = "Pedro Montero Vilar"
__copyright__   = "Copyright 2026, INTECMAR"
__license__     = "MIT"
__version__     = "0.1.0"
__maintainer__  = "Pedro Montero Vilar"
__email__       = "pmontero@intecmar.gal"
__status__      = "Development"

import os
import sys
import json
from dotenv import load_dotenv

# Add src to python path
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
    print("--- CTD_query: Multi-Variable Heatmap Generator ---")
    
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

    # 4. Processing parameters from config
    stations_to_process = common_cfg.get("stations", [])
    begin_date = common_cfg.get("begin_date")
    end_date = common_cfg.get("end_date")
    variables_to_process = common_cfg.get("variables", ["Temperatura", "Salinidad"])
    
    # Filter variables to exclude Depth/Pressure as they are coordinates for heatmaps
    variables_to_process = [v for v in variables_to_process if v not in ["Profundidad", "Presión"]]
    
    output_dir = heatmap_cfg.get("output_dir", "plots/heatmaps")
    os.makedirs(output_dir, exist_ok=True)

    # Fetch station metadata once for depths
    print("[*] Fetching station metadata...")
    all_stations = client.get_stations()
    station_metadata = {s['StationCode']: s for s in all_stations}

    for station in stations_to_process:
        print(f"[*] Processing Station: {station}")
        
        # Determine station depth and calculate limits
        station_depth_raw = 60 # Default
        if station in station_metadata:
            meta = station_metadata[station]
            if meta.get('Depth'):
                station_depth_raw = float(meta['Depth'])
                print(f"    [i] Station depth: {station_depth_raw}m")
        
        # New logic: eje de la grafica irá de top a (station_depth - bottom)
        top_limit = heatmap_cfg.get("top", 0)
        bottom_offset = heatmap_cfg.get("bottom", 0)
        final_depth_limit = station_depth_raw - bottom_offset
        
        print(f"    [i] Plotting depth range: {top_limit}m to {final_depth_limit}m")

        # 1. Fetch raw data
        all_fetch_vars = variables_to_process + ["Profundidad", "Presión"]
        raw_data = client.get_ctd_data(station, begin_date, end_date, all_fetch_vars)
        
        if not raw_data:
            print(f"    [!] No data found for station {station} in this period.")
            continue

        # 2. Process into domain models
        profiles = DataProcessor.process_raw_data(station, raw_data)
        
        if not profiles:
            print(f"    [!] No valid profiles found in response.")
            continue
            
        print(f"    [+] Found {len(profiles)} profiles. Generating heatmaps...")
        
        # Accumulate data for the heatmap plotter
        station_data = {}
        for p in profiles:
            flat_data = []
            for m in p.measurements:
                row = {}
                if m.depth is not None: row["Profundidad"] = m.depth
                if m.pressure is not None: row["Presión"] = m.pressure
                row.update(m.values)
                row.update(m.flags) 
                flat_data.append(row)
            station_data[p.timestamp] = flat_data

        # 3. Iterate over each variable and generate a heatmap
        for var in variables_to_process:
            print(f"    [>] Generating Heatmap for: {var}")
            
            c_map = heatmap_cfg.get("color_map", "coolwarm" if "temp" in var.lower() else "jet")
            
            plotter = CTDHeatmapPlotter(
                station=station,
                parameter_name=var,
                top=top_limit,
                depth=final_depth_limit,
                color_map=c_map,
                contour=heatmap_cfg.get("contour", True),
                measure_dots=heatmap_cfg.get("measure_dots", True)
            )

            filename = f"heatmap_{station}_{var.lower()}.png"
            output_path = os.path.join(output_dir, filename)
            
            if plotter.plot(station_data, output_path):
                print(f"    [OK] Generated: {filename}")
            else:
                print(f"    [FAIL] Skipping {var}")

if __name__ == "__main__":
    main()