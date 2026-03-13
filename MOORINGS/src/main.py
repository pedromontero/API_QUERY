# -*- coding: utf-8 -*-

"""
!==============================================================================!
!                OCXG API - CAPTA PROJECT (INTECMAR)                           !
!==============================================================================!
!                                                                              !
! TITLE        : OCXG API_QUERY                                                !
! PROJECT      : CAPTA                                                         !
! URL          : http://observatoriocosteiro.gal/es                            !
! AFFILIATION  : INTECMAR (Xunta de Galicia)                                   !
!                                                                              !
! DATE         : March 2026                                                    !
! VERSION      :  1.0.0                                                        !
! REVISION     : Montero 0.1                                                   !
!                                                                              !
! AUTHOR       : Pedro Montero Vilar                                           !
! CONTACT      : pmontero@intecmar.gal                                         !
!                                                                              !
! DESCRIPTION  : Executes the processing based on config.                      !
!                                                                              !
!==============================================================================!
!                               MIT LICENSE                                    !
!------------------------------------------------------------------------------!
! Copyright (c) 2026 INTECMAR                                                  !
!                                                                              !
! Permission is hereby granted, free of charge, to any person obtaining a copy !
! of this software and associated documentation files (the "Software"), to deal!
! in the Software without restriction, including without limitation the rights !
! to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    !
! copies of the Software, and to permit persons to whom the Software is        !
! furnished to do so, subject to the following conditions:                     !
!                                                                              !
! The above copyright notice and this permission notice shall be included in   !
! all copies or substantial portions of the Software.                          !
!                                                                              !
! THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   !
! IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     !
! FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  !
! AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       !
! LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,!
! OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN    !
! THE SOFTWARE.                                                                !
!------------------------------------------------------------------------------!
! Project CAPTA. Co-funded by the European Union through the Interreg VI-A     !
! Spain-Portugal (POCTEP) 2021-2027 Program. The opinions expressed are the    !
! sole responsibility of the author.                                           !
!==============================================================================!
"""

__author__      = "Pedro Montero Vilar"
__copyright__   = "Copyright 2026, INTECMAR"
__license__     = "MIT"
__version__      = "1.0.0"
__maintainer__  = "Pedro Montero Vilar"
__email__       = "pmontero@intecmar.gal"
__status__       = "Production"

import os
import json
from datetime import datetime
from api.mooring_client import MooringClient
from data.mooring_processor import MooringDataProcessor
from visualization.mooring_plotter import MooringPlotter

class MooringService:
    def __init__(self, base_url, user, password):
        self.client = MooringClient(base_url, user, password)
        self.processor = MooringDataProcessor()
        self.plotter = MooringPlotter(output_dir="plots")

    def run(self, config):
        """
        Executes the processing based on config.
        """
        stations = config.get("stations", [])
        begin_date = config.get("begin_date")
        end_date = config.get("end_date")
        variables = config.get("variables", [])
        frequency = config.get("frequency", "daily") # Default daily
        func = config.get("function", "AVG")

        # Map frequency to URL slugs if needed
        # In Swagger: 10minute, hourly, daily, monthly
        freq_map = {
            "10minute": "10minute",
            "hourly": "hourly",
            "daily": "daily",
            "monthly": "monthly",
            "10min": "10minute",
            "hour": "hourly",
            "day": "daily",
            "month": "monthly"
        }
        url_freq = freq_map.get(frequency.lower(), frequency)

        # Get stations metadata for names
        all_stations = self.client.get_stations()
        station_map = {s['StationCode']: s['StationName'] for s in all_stations}

        for station_code in stations:
            s_name = station_map.get(station_code, station_code)
            print(f"[*] Processing Station: {s_name} ({station_code})")

            # Get parameters for this station to resolve IDs
            available_params = self.client.get_station_parameters(station_code)
            
            # Map of Code/Name to ID
            # In Moorings, ParameterCode seems to be the ID (e.g. 20003) 
            # while ParameterName is the short string (e.g. TAU)
            param_identity_map = {}
            for p in available_params:
                code = str(p.get("ParameterCode"))
                name = str(p.get("ParameterName"))
                desc = str(p.get("Description", "")).lower()
                
                # Store all possible keys to match
                param_identity_map[code.lower()] = code
                param_identity_map[name.lower()] = code
                param_identity_map[desc] = code

            for var in variables:
                var_key = var.lower()
                param_id = param_identity_map.get(var_key)
                
                if not param_id:
                    print(f"    [!] Variable '{var}' not found for station {station_code}. Skipping.")
                    continue

                print(f"    [>] Fetching data for {var} (ID: {param_id})")
                try:
                    raw_data = self.client.get_mooring_data(
                        station_code, param_id, url_freq, begin_date, end_date, function=func
                    )
                    
                    if not raw_data:
                        print(f"    [i] No data for {var} in this range.")
                        continue
                        
                    batches = self.processor.process_raw_data(raw_data)
                    
                    if not batches:
                        print(f"    [!] Failed to process data for {var}.")
                        continue
                        
                    print(f"    [+] Plotting {len(batches)} series...")
                    plot_path = self.plotter.plot_time_series(batches, station_name=s_name)
                    if plot_path:
                        print(f"    [OK] Saved plot: {os.path.basename(plot_path)}")
                        
                except Exception as e:
                    print(f"    [ERR] Error processing {var}: {e}")