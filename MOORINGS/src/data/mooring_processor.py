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
! DESCRIPTION  : Processes raw Mooring data into high-level batches.           !
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

from datetime import datetime
from models.domain import MooringMeasurement, MooringBatch

class MooringDataProcessor:
    """
    Processes raw Mooring data into high-level batches.
    """
    
    @staticmethod
    def process_raw_data(raw_data):
        """
        Parses the list of objects returned by the Mooring data endpoint.
        
        Args:
            raw_data (list): List of objects (one per depth/configuration).
            
        Returns:
            list[MooringBatch]: List of processed batches.
        """
        batches = []
        if not raw_data or not isinstance(raw_data, list):
            return batches
            
        for entry in raw_data:
            metadata = entry
            samples = entry.get("Samples", [])
            
            if not samples:
                continue
                
            batch = MooringBatch(
                station_code=str(metadata.get("StationCode")),
                parameter_id=metadata.get("ParameterId"),
                parameter_name=metadata.get("ParameterCode", "Unknown"),
                units=metadata.get("Units", ""),
                frequency=metadata.get("Frequency", "unknown"),
                measurements=[]
            )
            
            depth = metadata.get("Depth")
            
            for s in samples:
                raw_date = s.get("Date")
                try:
                    # '2023-01-31T00:00:00Z'
                    dt = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                except:
                    dt = datetime.strptime(raw_date.split('T')[0], "%Y-%m-%d")
                    
                meas = MooringMeasurement(
                    timestamp=raw_date,
                    date_obj=dt,
                    value=float(s.get("Value", 0.0)),
                    flag=int(s.get("QualityCode", 0)),
                    depth=depth
                )
                batch.measurements.append(meas)
                
            # Sort measurements by date
            batch.measurements.sort(key=lambda x: x.date_obj)
            batches.append(batch)
            
        return batches