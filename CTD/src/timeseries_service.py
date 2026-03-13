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
! DESCRIPTION  : Orchestrates retrieval and processing of aggregated CTD data. !
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

import json
import os
import sys
from dotenv import load_dotenv
from api.ctd_client import CTDClient
from data.timeseries_processor import TimeseriesProcessor
from visualization.timeseries_plotter import TimeseriesPlotter

class CTDTimeseriesService:
    """
    Orchestrates the retrieval, processing, and visualization of aggregated CTD data (Time Series).
    """
    def __init__(self):
        load_dotenv()
        self.api_url = os.getenv("API_BASE_URL", "https://api.intecmar.gal")
        self.username = os.getenv("API_USER")
        self.password = os.getenv("API_PASSWORD")
        
        if not self.username or not self.password:
            # Fallback for local .env in the parent directory of standalone scripts
            load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
            self.username = os.getenv("API_USER")
            self.password = os.getenv("API_PASSWORD")

        if not self.username or not self.password:
            print("CRITICAL: API_USER and API_PASSWORD must be set in .env")
            sys.exit(1)
            
        self.client = CTDClient(self.api_url, self.username, self.password)

    def run(self, common_input="input.json", ts_input="input_timeseries.json"):
        """
        Main execution flow for time series.
        """
        script_dir = os.getcwd()
        if not os.path.exists(os.path.join(script_dir, common_input)):
            # If called from CTD subfolder
            script_dir = os.path.dirname(os.path.abspath(__file__)) # src/
            script_dir = os.path.dirname(script_dir) # CTD/
            
        common_path = os.path.join(script_dir, common_input)
        ts_path = os.path.join(script_dir, ts_input)

        if not os.path.exists(common_path):
            print(f"Error: Common input file {common_path} not found.")
            return

        with open(common_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        with open(ts_path, 'r', encoding='utf-8') as f:
            ts_config = json.load(f)

        # 1. Get valid aggregation types (visible only)
        try:
            all_agg_types = self.client.get_aggregation_types()
            visible_agg_codes = [a['Code'] for a in all_agg_types if a.get('Visible')]
        except Exception as e:
            print(f"Error fetching aggregation types: {e}")
            return

        requested_aggs = ts_config.get("aggregation_types", [])
        aggs_to_use = [a for a in requested_aggs if a in visible_agg_codes]
        
        if not aggs_to_use:
            print("Error: None of the requested aggregation types are visible or valid.")
            return

        # 2. Setup components
        plotter = TimeseriesPlotter(ts_config.get("output_dir", "plots/timeseries"))
        
        begin_date = config.get("begin_date")
        end_date = config.get("end_date")
        stations = config.get("stations", [])
        variables = config.get("variables", [])
        y_axis_config = ts_config.get("y_axis", {})

        print(f"--- Starting CTD Time Series Recovery ({begin_date} to {end_date}) ---")

        for station in stations:
            print(f"[*] Processing Station: {station}")
            all_data = []
            for agg in aggs_to_use:
                try:
                    raw_data = self.client.get_aggregated_data(station, agg, begin_date, end_date, variables)
                    if raw_data:
                        all_data.extend(raw_data)
                except Exception as e:
                    print(f"    [!] Error fetching {agg} for {station}: {e}")

            if not all_data:
                continue

            # 3. Process
            df = TimeseriesProcessor.to_dataframe(all_data)
            
            # 4. Plot
            found_parameters = df['ParameterName'].unique()
            for param in found_parameters:
                y_limits = "auto"
                for k, v in y_axis_config.items():
                    if k.lower() in param.lower():
                        y_limits = v
                        break
                
                plot_path = plotter.plot_timeseries(df[df['ParameterName'] == param], station, param, y_limits)
                if plot_path:
                    print(f"    [OK] Time series saved: {plot_path}")
