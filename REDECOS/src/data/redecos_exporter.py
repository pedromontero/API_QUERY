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
! DESCRIPTION  : Handles exporting Redecos batches to structured Excel files.  !
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
import pandas as pd

class RedecosExporter:
    """
    Handles exporting Redecos batches to structured Excel files.
    """
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_station_excel(self, batches, station_code, station_name="Station"):
        """
        Combines multiple parameter batches into one Excel file per station.
        Columns: [Time, Param1, Flag1, Param2, Flag2, ...]
        """
        if not batches:
            return None

        master_df = None
        
        for batch in batches:
            param = batch.parameter_name
            val_col = f"{param}"
            flag_col = f"{param}_Flag"
            
            # Filter Flag 9 (consistent with Mooring/Requirement)
            data = []
            for m in batch.measurements:
                if m.flag == 9:
                    continue
                data.append({
                    "Date (UTC)": m.timestamp,
                    val_col: m.value,
                    flag_col: m.flag
                })
            
            df = pd.DataFrame(data)
            if df.empty:
                continue
                
            df.set_index("Date (UTC)", inplace=True)
            
            if master_df is None:
                master_df = df
            else:
                # Outer join uses index (Time) to merge
                master_df = master_df.join(df, how="outer")

        if master_df is None or master_df.empty:
            return None

        # Sort and clean index
        master_df.index = pd.to_datetime(master_df.index)
        if master_df.index.tz is not None:
            master_df.index = master_df.index.tz_localize(None)
        master_df.sort_index(inplace=True)

        filename = f"redecos_{station_code}_{station_name.lower().replace(' ', '_')}.xlsx"
        output_path = os.path.join(self.output_dir, filename)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            master_df.to_excel(writer, sheet_name="Redecos Data")
            # Auto-adjust column widths
            worksheet = writer.sheets['Redecos Data']
            # Header column (index)
            worksheet.column_dimensions['A'].width = 25
            for i, col in enumerate(master_df.columns):
                column_len = max(master_df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(66 + i)].width = column_len

        return output_path