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
            return getattr(Parameter, name)()
        except AttributeError:
            method_list = [method for method in dir(Parameter) if not (method.startswith('__') or method.startswith('get'))]
            print(f'\nERROR: There is not a parameter called "{name}".')
            print('\nIncluded parameters are: ')
            for method in method_list:
                print(f'\t- {method}')
            return None

    @staticmethod
    def get_by_name_es(name_es):
        """Get a Parameter object from parameter Spanish name."""
        method_list = [method for method in dir(Parameter) if not (method.startswith('__') or method.startswith('get'))]
        for method in method_list:
            method_object = Parameter.get_by_name(method)
            if method_object and method_object.name_es == name_es:
                return method_object
        return None

    def get_label(self):
        return f"{self.name_en} ({self.units})"
