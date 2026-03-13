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
! DESCRIPTION  : Handles generation of high-quality time series plots.         !
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

import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

class TimeseriesPlotter:
    """
    Handles generation of high-quality time series plots for aggregated data.
    """
    def __init__(self, plots_dir):
        self.plots_dir = plots_dir
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        
        # Set a premium theme
        sns.set_theme(style="whitegrid", context="talk", palette="deep")

    def plot_timeseries(self, df, station_code, parameter_name, y_limits=None):
        """
        Creates a time series plot for a specific parameter and station.
        Supports multiple aggregation types in the same plot.
        """
        if df.empty:
            return None

        plt.figure(figsize=(15, 8))
        
        # Sort by date for proper line plotting
        df = df.sort_values(by='CastDate')
        
        # Unique aggregation types in this data
        agg_types = df['Agregacion'].unique()
        
        # Plot each aggregation type
        for agg in agg_types:
            agg_data = df[df['Agregacion'] == agg]
            plt.plot(agg_data['CastDate'], agg_data['Value'], 
                     marker='o', markersize=4, label=agg, linewidth=2, alpha=0.9)

        # Aesthetics
        plt.title(f"CTD Time Series - Station {station_code}\nParameter: {parameter_name}", 
                  fontsize=18, fontweight='bold', pad=20)
        plt.xlabel("Date", fontsize=14, fontweight='semibold')
        plt.ylabel(parameter_name, fontsize=14, fontweight='semibold')
        
        # Grid and spines
        plt.grid(True, linestyle='--', alpha=0.7)
        sns.despine(trim=True)
        
        plt.legend(title="Aggregation", loc='best', frameon=True, shadow=True)
        
        # Y axis limits
        if y_limits and isinstance(y_limits, dict):
            min_val = y_limits.get('min')
            max_val = y_limits.get('max')
            if min_val is not None and max_val is not None:
                plt.ylim(min_val, max_val)
            elif min_val is not None:
                plt.ylim(bottom=min_val)
            elif max_val is not None:
                plt.ylim(top=max_val)

        # Fix overlapping dates
        plt.gcf().autofmt_xdate()
        
        plt.tight_layout()

        # Save plot
        clean_param = parameter_name.replace("/", "_").replace(" ", "_")
        filename = f"timeseries_{station_code}_{clean_param}.png"
        filepath = os.path.join(self.plots_dir, filename)
        plt.savefig(filepath, dpi=200, bbox_inches='tight')
        plt.close()
        
        return filepath
