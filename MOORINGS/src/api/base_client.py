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
! DESCRIPTION  : Base client for interacting with the Intecmar API.
    Han... !
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