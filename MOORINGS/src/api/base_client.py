"""
Author: Pedro Montero
Organization: INTECMAR
License: Open Source
"""

import requests
import time
from abc import ABC

class BaseIntecmarClient(ABC):
    """
    Base client for interacting with the Intecmar API.
    Handles authentication and generic request logic.
    """
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.token_expiry = 0

    def _authenticate(self):
        """
        Obtains an OAuth2 token using the password flow.
        """
        auth_url = f"{self.base_url}/auth/user_token"
        data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        response = requests.post(auth_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data.get("access_token")
        # Token typically lasts 3600 seconds, we refresh 5 mins before
        expires_in = token_data.get("expires_in", 3600)
        self.token_expiry = time.time() + expires_in - 300

    def _get_headers(self):
        """
        Returns the authorization headers, refreshing the token if necessary.
        """
        if not self.token or time.time() > self.token_expiry:
            self._authenticate()
        
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def _get(self, endpoint, params=None):
        """
        Generic GET request with authentication.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
