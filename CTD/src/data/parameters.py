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
! DESCRIPTION  : Class for parameter attributes used in plotting.              !
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

from dataclasses import dataclass
import numpy as np

@dataclass
class Parameter:
    """Class for parameter attributes used in plotting."""
    name: str = ''
    units: str = ''
    name_en: str = ''
    name_es: str = ''
    name_gl: str = ''
    name_sbd: str = ''
    acronym: str = ''
    color_map: str = 'jet'
    scale_map: list = None
    contour: bool = True
    measure_dots: bool = False
    cleaners: list = None

    def __post_init__(self):
        if self.cleaners is None:
            self.cleaners = []
        if self.scale_map is None:
            self.scale_map = []

    @staticmethod
    def temperature():
        return Parameter(name='sea_water_temperature',
                         units='ºC',
                         name_en='Temperature',
                         name_es='Temperatura',
                         name_gl='Temperatura',
                         name_sbd='TEMP',
                         acronym='T',
                         color_map='coolwarm',
                         scale_map=[n for n in np.arange(10., 23.5, 0.5)],
                         contour=True,
                         measure_dots=False)

    @staticmethod
    def salinity():
        return Parameter(name='sea_water_salinity',
                         units='',
                         name_en='Salinity',
                         name_es='Salinidad',
                         name_gl='Salinidade',
                         name_sbd='PSAL',
                         acronym="S",
                         color_map='jet',
                         scale_map=[n for n in np.arange(28., 37, 0.5)],
                         contour=True,
                         measure_dots=False)

    @staticmethod
    def pressure():
        return Parameter(name='sea_water_pressure',
                         units='db',
                         name_en='Pressure',
                         name_es='Presión',
                         name_gl='Presión',
                         name_sbd='prSM',
                         acronym="P",
                         color_map='cool',
                         scale_map=[n for n in np.arange(0, 100, 1)],
                         contour=True,
                         measure_dots=False)

    @staticmethod
    def oxygen():
        return Parameter(name='sea_water_oxygen',
                         units='ml/l',
                         name_en='Oxygen',
                         name_es='Oxígeno',
                         name_gl='Osíxeno',
                         name_sbd='oxygen_ml_L',
                         acronym="O",
                         color_map='hot_r',
                         scale_map=[n for n in np.arange(2., 8., 0.2)],
                         contour=True,
                         measure_dots=False)

    @staticmethod
    def ph():
        return Parameter(name='sea_water_ph',
                         units='1',
                         name_en='pH',
                         name_es='pH',
                         name_gl='pH',
                         name_sbd='ph',
                         acronym="ph",
                         color_map='jet',
                         scale_map=[n for n in np.arange(7., 9., 0.05)],
                         contour=False,
                         measure_dots=False)

    @staticmethod
    def depth():
        return Parameter(name='sea_water_depth',
                         units='m',
                         name_en='Depth',
                         name_es='Profundidad',
                         name_gl='Profundidade',
                         name_sbd='DEPTH',
                         acronym="DEP",
                         color_map='jet',
                         scale_map=[n for n in np.arange(0., 100., 0.25)],
                         contour=False,
                         measure_dots=False)

    @staticmethod
    def get_by_name(name):
        """Get a Parameter object from parameter method name."""
        try:
            attr = getattr(Parameter, name)
            if callable(attr):
                return attr()
            return None
        except AttributeError:
            return None

    @staticmethod
    def get_by_name_es(name_es):
        """Get a Parameter object from parameter Spanish name."""
        # Methods to check
        methods = ['temperature', 'salinity', 'oxygen', 'ph', 'depth', 'pressure']
        for method in methods:
            p = Parameter.get_by_name(method)
            if p and p.name_es == name_es:
                return p
        return None

    def get_label(self):
        return f"{self.name_en} ({self.units})"