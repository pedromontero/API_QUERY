# -*- coding: utf-8 -*-

#    !------------------------------------------------------------------------------
#    !                       OCXG API, CAPTA Project
#    !------------------------------------------------------------------------------
#    !
#    ! TITLE         : OCXG API_QUERY
#    ! PROJECT       : CAPTA
#    ! URL           : http://observatoriocosteiro.gal/es
#    ! AFFILIATION   : INTECMAR
#    ! DATE          : March 2026
#    ! REVISION      : Montero 0.1
#    !> @author
#    !> Pedro Montero Vilar
#    !
#    ! DESCRIPTION:
#    ! Preprocessing script for collecting data from OCXG API and processing them
#    !--------------------------------------------------------------------------------------
#
#    MIT License
#
#    Copyright (c) 2026 INTECMAR
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

from .base_client import BaseIntecmarClient

class CTDClient(BaseIntecmarClient):
    """
    Client for CTD-specific endpoints in the Intecmar API.
    """
    
    def get_stations(self):
        """
        Retrieves all CTD stations.
        """
        return self._get("ctd/stations")

    def get_stations_by_survey(self, survey_id):
        """
        Retrieves stations sampled in a specific survey.
        """
        return self._get(f"ctd/stations/survey/{survey_id}")

    def get_surveys(self, begin_date, end_date):
        """
        Retrieves surveys conducted between two dates.
        """
        return self._get(f"ctd/survey/{begin_date}/{end_date}")

    def get_ctd_data(self, station_code, begin_date, end_date, parameters=None):
        """
        Retrieves CTD profile data for a station.
        """
        params = {
            "begin_date": begin_date,
            "end_date": end_date,
            "format": "JSON"
        }
        if parameters:
            params["parameter"] = parameters
            
        return self._get(f"ctd/data/{station_code}", params=params)
