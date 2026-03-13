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
! DESCRIPTION  : Logic for transforming raw API responses into domain models.  !
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

from models.domain import CTDProfile, Measurement
from typing import List, Dict, Any

class DataProcessor:
    """
    Logic for transforming raw API responses into domain models.
    """
    
    @staticmethod
    def process_raw_data(station_code: str, raw_data: Any) -> List[CTDProfile]:
        """
        Processes the hierarchical CTD data from the API.
        raw_data can be a list of profiles or a single profile dictionary.
        """
        if isinstance(raw_data, dict):
            raw_data = [raw_data]
            
        profiles: List[CTDProfile] = []
        
        for profile_data in raw_data:
            if not isinstance(profile_data, dict):
                continue
            
            timestamp = profile_data.get('SamplingDate') or profile_data.get('Date') or profile_data.get('CastDate')
            if not timestamp:
                continue
                
            profile = CTDProfile(station_code=station_code, timestamp=timestamp)
            
            measurements_list = profile_data.get('Measurements') or profile_data.get('Scans') or []
            for m_item in measurements_list:
                # Some versions have 'Parameters', others have data flat or in other keys
                params = m_item.get('Parameters')
                if params is None:
                    # If flat, omit metadata keys
                    params = {k: v for k, v in m_item.items() if k not in ['Scan', 'Presion', 'Profundidad']}
                
                # Extract depth and pressure
                depth_obj = params.get('Profundidad', {})
                pres_obj = params.get('Presión') or params.get('Presi\u00f3n') or params.get('Presion', {})
                
                # Check if it's the dict structure or flat value
                def get_val(obj):
                    if isinstance(obj, dict): return obj.get('Value')
                    return obj

                depth = get_val(depth_obj)
                pressure = get_val(pres_obj)
                
                values_with_flags = {}
                
                for var_name, var_data in params.items():
                    if var_name in ['Profundidad', 'Presión', 'Presi\u00f3n', 'Presion']:
                        continue
                    
                    if isinstance(var_data, dict):
                        val = var_data.get('Value')
                        flag = var_data.get('QualityFlag')
                        units = var_data.get('Units', '')
                        
                        col_name = f"{var_name} ({units})" if units else var_name
                        values_with_flags[col_name] = val
                        values_with_flags[f"{col_name}_Flag"] = flag
                    else:
                        values_with_flags[var_name] = var_data
                
                measurement = Measurement(
                    depth=float(depth) if depth is not None else None,
                    pressure=float(pressure) if pressure is not None else None,
                    values=values_with_flags,
                    flags={} # We now store flags directly in values for ordering
                )
                profile.measurements.append(measurement)
            
            profiles.append(profile)
            
        return profiles