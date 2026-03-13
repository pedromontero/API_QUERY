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
! VERSION      : 0.1.0-alpha                                                   !
! REVISION     : Montero 0.1                                                   !
!                                                                              !
! AUTHOR       : Pedro Montero Vilar                                           !
! CONTACT      : pmontero@intecmar.gal                                         !
!                                                                              !
! DESCRIPTION  : Handles generation of CTD profile plots.                      !
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
!------------------------------------------------------------------------------!
! Project CAPTA. Co-funded by the European Union through the Interreg VI-A     !
! Spain-Portugal (POCTEP) 2021-2027 Program. The opinions expressed are the    !
! sole responsibility of the author.                                           !
!==============================================================================!
"""

__author__      = "Pedro Montero Vilar"
__copyright__   = "Copyright 2026, INTECMAR"
__license__     = "MIT"
__version__     = "0.1.0"
__maintainer__  = "Pedro Montero Vilar"
__email__       = "pmontero@intecmar.gal"
__status__      = "Development"

import matplotlib.pyplot as plt
import os
import pandas as pd

class ProfilePlotter:
    """
    Handles generation of CTD profile plots.
    """
    def __init__(self, plots_dir):
        self.plots_dir = plots_dir
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)

    def plot_profile(self, station_code, date_str, data, time_str=None, only_good_data=False, scaled_plots=False, custom_scales=None):
        """
        Creates a plot for a single CTD profile with one subplot per variable.
        Uses advanced aesthetics for a premium look.
        """
        df = pd.DataFrame(data)
        if df.empty:
            return

        # Try to apply a clean style
        try:
            import seaborn as sns
            sns.set_theme(style="whitegrid", context="talk")
        except ImportError:
            plt.style.use('bmh')

        # Determine Y axis (Prefer Depth, then Pressure)
        y_axis = None
        if "Profundidad" in df.columns:
            y_axis = "Profundidad"
        elif "Presión" in df.columns:
            y_axis = "Presión"

        if not y_axis:
            return

        # Filter out NaN in Y axis
        df = df.dropna(subset=[y_axis])
        df = df.sort_values(by=y_axis)

        # Variables to plot (exclude Y axis, flags and Pressure if Y is Depth)
        exclude = [y_axis, "Presión", "Presi\u00f3n", "Presion"]
        variables = [c for c in df.columns if c not in exclude and not str(c).endswith("_Flag")]

        if not variables:
            return

        # Create subplots
        n_vars = len(variables)
        fig, axes = plt.subplots(1, n_vars, figsize=(4 * n_vars + 2, 10), sharey=True)
        
        # Ensure axes is iterable even if only one variable
        if n_vars == 1:
            axes = [axes]
        
        # Use a professional color palette
        palette = plt.cm.Dark2.colors if n_vars <= 8 else plt.cm.tab20.colors
        custom_scales = custom_scales or {}
        
        for i, var in enumerate(variables):
            ax = axes[i]
            color = palette[i % len(palette)]
            
            # Filter data for this subplot
            clean_df = df.dropna(subset=[var])
            
            # Case-insensitive flag check and stripping units
            clean_var_name = var.split(' (')[0]
            flag_col = next((c for c in df.columns if c.startswith(clean_var_name) and c.endswith("_Flag")), None)

            if only_good_data and flag_col:
                # Keep only points where QualityFlag is not 4 (Bad)
                clean_df = clean_df[clean_df[flag_col] != 4]
            
            if clean_df.empty:
                ax.text(0.5, 0.5, f"No qualitative\ndata for\n{var}", 
                        ha='center', va='center', color='gray', fontsize=10, transform=ax.transAxes)
            else:
                # Main continuous line with markers (Style of before)
                ax.plot(clean_df[var], clean_df[y_axis], marker='o', markersize=3, 
                        color=color, linewidth=2, alpha=0.8, zorder=2, label=var)
                
                # Overlay special markers for No Control (Flag 0) -> Hollow markers
                if flag_col in clean_df.columns:
                    no_control = clean_df[clean_df[flag_col] == 0]
                    if not no_control.empty:
                        ax.plot(no_control[var], no_control[y_axis], marker='o', markersize=4, 
                                markeredgecolor=color, markerfacecolor='white', linestyle='', 
                                markeredgewidth=1.5, zorder=3)

                # Overlay special markers for Bad Data (Flag 4) -> Black markers
                if not only_good_data and flag_col in clean_df.columns:
                    bad_data = clean_df[clean_df[flag_col] == 4]
                    if not bad_data.empty:
                        ax.plot(bad_data[var], bad_data[y_axis], marker='x', markersize=5, 
                                color='black', linestyle='', zorder=4)
            
            # Apply custom scaling if requested
            if scaled_plots and clean_var_name in custom_scales:
                limits = custom_scales[clean_var_name]
                ax.set_xlim(limits[0], limits[1])
            
            ax.set_xlabel(var, fontweight='bold', fontsize=12)
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            if i == 0:
                ax.set_ylabel(f"{y_axis} (m)" if y_axis == "Profundidad" else f"{y_axis} (db)", 
                             fontweight='bold', fontsize=12)
                ax.invert_yaxis()

        title = f"CTD_query: Profile Analysis\nStation: {station_code} | Date: {date_str}"
        if time_str:
            title += f" {time_str} UTC"
            
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.93])

        filename = f"{date_str.replace('-', '')}_{station_code}.png"
        filepath = os.path.join(self.plots_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath