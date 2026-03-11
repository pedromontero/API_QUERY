"""
2D Time Series Plotting Engine for CTD Data.
Handles interpolation and heatmap generation.
"""

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num, DateFormatter, MonthLocator
import os

def cm_to_inch(value):
    """Convert centimeters to inches."""
    return value / 2.54

def prepare_plot(font=12):
    """Configure matplotlib global settings."""
    plt.switch_backend('Agg')
    plt.rcParams.update({'font.size': font})

class PlotFrame:
    """Defines the boundaries and aspect ratio of the plot."""
    def __init__(self, date, y, **kwargs):
        self.min_x = date2num(kwargs.get('start', min(date)))
        self.max_x = date2num(kwargs.get('end', max(date)))
        self.min_y = kwargs.get('top', min(y))
        self.max_y = kwargs.get('depth', max(y))

    def get_aspect(self, ratio):
        """Calculate aspect ratio for the plot."""
        return ratio * ((self.max_x - self.min_x) / (self.max_y - self.min_y))

    def apply_limits(self, ax):
        """Apply the calculated limits to a matplotlib axis."""
        ax.set_xlim(self.min_x, self.max_x)
        ax.set_ylim(self.max_y, self.min_y)

class TimeSeries2D:
    """Generates 2D heatmaps (Time vs. Depth) using CTD data."""
    def __init__(self, date, var, y):
        self.date = date
        self.var = var
        self.y = y
        self.station = "Default"

    def plot(self, parameter, file_out, **kwargs):
        prepare_plot()
        fig, ax = plt.subplots(figsize=(cm_to_inch(25), cm_to_inch(12)), constrained_layout=True)

        frame = PlotFrame(self.date, self.y, **kwargs)
        x_grid, y_grid, z_grid = self.define_grid(frame)
        frame.apply_limits(ax)

        # Plot heatmap
        if parameter.scale_map:
            levels = parameter.scale_map
        else:
            levels = 20

        im = ax.contourf(x_grid, y_grid, z_grid, levels, cmap=parameter.color_map)
        plt.colorbar(im, ax=ax, orientation='horizontal', fraction=0.05, aspect=40, shrink=0.8, label=parameter.get_label())

        if parameter.contour:
            ax.contour(x_grid, y_grid, z_grid, levels, linewidths=0.5, colors='k', alpha=0.3)

        if parameter.measure_dots:
            ax.scatter(date2num(self.date), self.y, marker='o', c='k', s=0.5, alpha=0.2)

        if kwargs.get('ratio'):
            ax.set_aspect(frame.get_aspect(kwargs.get('ratio')))

        ax.set_title(f"CTD Heatmap: {self.station}\nVariable: {parameter.name_es}", fontweight='bold', pad=10)
        self.format_axis(ax)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_out)), exist_ok=True)
        
        fig.savefig(file_out, dpi=150, facecolor='w', edgecolor='w', orientation='landscape')
        plt.close()

    def format_axis(self, ax):
        ax.xaxis.set_major_locator(MonthLocator(interval=2))
        ax.xaxis.set_minor_locator(MonthLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
        ax.set_xlabel("Date (UTC)", fontweight='bold')
        ax.set_ylabel("Depth (m)", fontweight='bold')

    def define_grid(self, limits):
        """Define the grid and interpolate data."""
        # Use more points for a smoother look
        x_grid, y_grid = np.mgrid[limits.min_x:limits.max_x:300j, limits.min_y:limits.max_y:150j]
        z_grid = griddata((date2num(self.date), self.y), self.var, (x_grid, y_grid), method='linear')
        return x_grid, y_grid, z_grid
