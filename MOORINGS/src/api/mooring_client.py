"""
Client for Mooring-specific endpoints in the Intecmar API.
"""

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
