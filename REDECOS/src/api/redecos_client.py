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
! DESCRIPTION  : Client specifically for REDECOS (Coastal Observatory Netwo... !
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

from .base_client import BaseIntecmarClient

class RedecosClient(BaseIntecmarClient):
    """
    Client specifically for REDECOS (Coastal Observatory Network) data.
    """
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)

    def get_stations(self):
        """Returns a list of REDECOS stations."""
        return self._get("/redecos/station")

    def get_station_description(self):
        """Returns detailed description for all REDECOS stations."""
        return self._get("/redecos/station/description")

    def get_parameters(self):
        """Returns a list of available parameters for the REDECOS network."""
        return self._get("/redecos/parameter")

    def get_station_data(self, station_code, parameter_name, begin_date, end_date):
        """
        Retrieves time series data for a specific station and parameter.
        The API expects: /redecos/station/{station_code}/parameter/data/{begin_date}/{end_date}
        with parameter_name as a query parameter.
        """
        endpoint = f"/redecos/station/{station_code}/parameter/data/{begin_date}/{end_date}"
        params = {"parameter_name": parameter_name}
        return self._get(endpoint, params=params)