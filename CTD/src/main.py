# -*- coding: utf-8 -*-

#    !------------------------------------------------------------------------------
#    !                       OCXG API, CAPTA Project
#    !------------------------------------------------------------------------------
#    !
#    ! TITLE         : OCXG API_QUERY
#    ! PROJECT       : CAPTA
#    ! URL           : http://observatoriocosteiro.gal/es
#    ! AFFILIATION   : INTECMAR
#    ! DATE          : March 2026
#    ! REVISION      : Montero 0.1
#    !> @author
#    !> Pedro Montero Vilar
#    !
#    ! DESCRIPTION:
#    ! Preprocessing script for collecting data from OCXG API and processing them
#    !--------------------------------------------------------------------------------------
#
#    MIT License
#
#    Copyright (c) 2026 INTECMAR
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

import json
import os
import sys
from dotenv import load_dotenv
from api.ctd_client import CTDClient
from data.processor import DataProcessor
from data.exporter import ExcelExporter
from visualization.plotter import ProfilePlotter

class CTDService:
    """
    Orchestrates the retrieval, processing, and visualization of CTD data.
    Follows SOLID principles and OO design.
    """
    def __init__(self):
        load_dotenv()
        self.api_url = os.getenv("API_BASE_URL", "https://api.intecmar.gal")
        self.username = os.getenv("API_USER")
        self.password = os.getenv("API_PASSWORD")
        
        if not self.username or not self.password:
            print("CRITICAL: API_USER and API_PASSWORD must be set in .env")
            sys.exit(1)
            
        self.client = CTDClient(self.api_url, self.username, self.password)
        self.exporter = ExcelExporter("output")
        self.plotter = ProfilePlotter("plots")

    def run(self, common_input="input.json", export_input="input_export.json", plots_input="input_plots.json"):
        """
        Main execution flow.
        """
        if not os.path.exists(common_input):
            print(f"Error: Common input file {common_input} not found.")
            return

        with open(common_input, 'r', encoding='utf-8') as f:
            config = json.load(f)

        begin_date = config.get("begin_date")
        end_date = config.get("end_date")
        station_codes = config.get("stations", [])
        variables = config.get("variables", ["Temperatura", "Salinidad"])
        
        # Always request Depth and Pressure as they are required for plotting and by user request
        for req in ["Profundidad", "Presión"]:
            if req not in variables:
                variables.append(req)

        # Component specific configs
        export_config = {}
        if os.path.exists(export_input):
            with open(export_input, 'r', encoding='utf-8') as f:
                export_config = json.load(f)
        
        plots_config = {}
        if os.path.exists(plots_input):
            with open(plots_input, 'r', encoding='utf-8') as f:
                plots_config = json.load(f)

        # Plotting specific settings from plots_config
        only_good_data = plots_config.get("only_good_data", False)
        scaled_plots = plots_config.get("scaled_plots", False)
        custom_scales = plots_config.get("custom_scales", {})

        # Initialize components with their specific configs
        exporter = ExcelExporter(export_config.get("output_dir", "output"))
        plotter = ProfilePlotter(plots_config.get("plots_dir", "plots"))

        # Basic validation
        if not begin_date or not end_date or not station_codes:
            print("Error: Invalid configuration in input.json. Check dates and stations.")
            return

        print(f"--- Starting CTD Data Recovery ({begin_date} to {end_date}) ---")

        for station in station_codes:
            print(f"[*] Processing Station: {station}")
            try:
                # 1. Fetch raw data
                raw_data = self.client.get_ctd_data(station, begin_date, end_date, variables)
                
                if not raw_data:
                    print(f"    [!] No data found for station {station} in this period.")
                    continue

                # 2. Process into domain models
                profiles = DataProcessor.process_raw_data(station, raw_data)
                
                if not profiles:
                    print(f"    [!] No valid profiles found in response.")
                    continue

                # 3. Prepare for export and visualization
                export_profiles = []
                for profile in profiles:
                    print(f"    [+] Profile found: {profile.timestamp}")
                    
                    # Convert measurements list of objects to list of dicts for pandas
                    flat_data = []
                    for m in profile.measurements:
                        row = {}
                        if m.depth is not None: row["Profundidad"] = m.depth
                        if m.pressure is not None: row["Presión"] = m.pressure
                        row.update(m.values)
                        row.update(m.flags)
                        flat_data.append(row)
                    
                    export_profiles.append({
                        'date': profile.date_str,
                        'time': profile.time_str,
                        'data': flat_data
                    })
                    
                    # 4. Generate visualization
                    plotter.plot_profile(
                        station, 
                        profile.date_str, 
                        flat_data, 
                        time_str=profile.time_str,
                        only_good_data=only_good_data,
                        scaled_plots=scaled_plots,
                        custom_scales=custom_scales
                    )

                # 5. Export to Excel
                exporter.export_station_data(station, export_profiles)
                print(f"    [OK] Excel and plots generated for {station}.")

            except Exception as e:
                print(f"    [ERROR] Failed to process station {station}: {e}")

if __name__ == "__main__":
    service = CTDService()
    service.run()
