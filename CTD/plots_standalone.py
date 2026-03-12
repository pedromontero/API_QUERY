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
! DESCRIPTION  : Standalone script for Plots.                                  !
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