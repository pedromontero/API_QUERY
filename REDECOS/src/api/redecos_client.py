"""
Redecos Client for Intecmar API.
Author: Pedro Montero
Organization: INTECMAR
"""

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
