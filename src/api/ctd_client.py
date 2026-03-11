"""
Author: Pedro Montero
Organization: INTECMAR
License: Open Source
"""

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
