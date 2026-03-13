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
! DESCRIPTION  : Handles exporting CTD data to Excel files.                    !
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
__version__     = "0.1.0"
__maintainer__  = "Pedro Montero Vilar"
__email__       = "pmontero@intecmar.gal"
__status__      = "Development"

import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

class ExcelExporter:
    """
    Handles exporting CTD data to Excel files.
    """
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def export_station_data(self, station_code, profiles_data):
        """
        Exports multiple profiles for a single station into one Excel file.
        Each profile goes into a separate sheet named YYYYMMDD.
        profiles_data: List of dicts, each with 'date', 'time', and 'data' (list of dicts)
        """
        file_path = os.path.join(self.output_dir, f"CTD_{station_code}.xlsx")
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for profile in profiles_data:
                date_str = profile['date'] # Expected YYYY-MM-DD
                sheet_name = date_str.replace('-', '')
                time_str = profile.get('time', '00:00:00')
                
                df = pd.DataFrame(profile['data'])
                
                # Ensure Depth and Pressure are first (if they exist)
                cols = list(df.columns)
                fixed_cols = []
                for p in ["Profundidad", "Presión"]:
                    if p in cols:
                        fixed_cols.append(p)
                        cols.remove(p)
                
                final_cols = fixed_cols + cols
                df = df[final_cols]
                
                # Write to sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)
                
                # Add custom header
                workbook = writer.book
                worksheet = workbook[sheet_name]
                worksheet['A1'] = f"Station: {station_code}"
                worksheet['A2'] = f"Date: {date_str} Time: {time_str}"
                
                # We could add units here if the API provides them, 
                # but based on docs it's usually just variable names.
                # If variables are like "Temperatura (ºC)", they are already in columns.