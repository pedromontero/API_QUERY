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
! DESCRIPTION  : Client for Mooring-specific endpoints.                        !
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

from .base_client import BaseIntecmarClient

class MooringClient(BaseIntecmarClient):
    """
    Client for Mooring-specific endpoints.
    """
    
    def get_stations(self):
        """Retrieves list of all mooring stations."""
        return self._get("moorings/station")

    def get_station_detail(self, station_code):
        """Retrieves general details for a specific station."""
        return self._get(f"moorings/station/{station_code}")

    def get_station_parameters(self, station_code):
        """Retrieves parameters available for a specific station."""
        return self._get(f"moorings/station/{station_code}/parameter")

    def get_station_sensors(self, station_code):
        """Retrieves sensors available for a specific station."""
        return self._get(f"moorings/station/{station_code}/sensor")

    def get_parameter_list(self):
        """Retrieves the full list of mooring parameters."""
        # Swagger shows both /moorings/parameter and /moorings/sensor
        return self._get("moorings/parameter")

    def get_mooring_data(self, station_code, parameter_id, frequency, 
                         begin_date, end_date, function="AVG"):
        """
        Retrieves historical data for a specific station and parameter.
        
        Args:
            station_code: Identification of the station.
            parameter_id: ID of the parameter.
            frequency: '10minute', 'hourly', 'daily', or 'monthly'.
            begin_date: 'YYYY-MM-DD'
            end_date: 'YYYY-MM-DD'
            function: Aggregation function (default 'AVG').
        """
        params = {
            "begin_date": begin_date,
            "end_date": end_date,
            "format": "JSON",
            "function": function
        }
        endpoint = f"moorings/data/{station_code}/{parameter_id}/{frequency}"
        return self._get(endpoint, params=params)