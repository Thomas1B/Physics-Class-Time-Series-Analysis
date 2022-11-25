'''
Module for handling custom plotting functions


'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
from .myData import getStationInfo


def plot_heatmap(data,
                 title='',
                 style='pcolor',
                 fontsize=12,
                 axisLimits=False):
    '''
    Function to plot a heat map after apply a scipy griddata.

    Parameters:
        data (tuple): (xi, yi, zi, coastline, locs) *see applyGrid()
        title (str): title of map.
        style (str): style used for coloring map (pcolor, contourf) default pcolor.
        fontsize (int): fontsize to use for labels default 12.
        axisLimits (bool): to apply axis limits on the plot, default False.
    '''
    xi, yi, zi, VI_coast, stations = data

    # Creating the Heatmap
    ax = plt.axes()
    ax.set_facecolor('steelblue') # coloring ocean.

    plt.plot(VI_coast.long, VI_coast.lat, color="k", linewidth=0.5) # plotting land
    plt.fill(VI_coast.long, VI_coast.lat, zorder=0, color="olivedrab") # coloring land


    # Coloring heat map
    cmap = plt.get_cmap('jet')
    if  style == 'contourf':
        c = plt.contourf(xi, yi, zi, 15, cmap=cmap)
    else:
        c = plt.pcolor(xi, yi, zi, cmap=cmap)

    plt.colorbar(c) # adding a color bar.
    plt.scatter(stations.long, stations.lati, color='white', edgecolor='r', label='Station')  # plotting station locations.

    # limits for plot
    if axisLimits:
        station_info = getStationInfo()
        maxs = station_info.max()[1:3] + 0.05
        mins = station_info.min()[1:3] - 0.05
        plt.xlim(mins.long)
        plt.ylim(mins.lati, maxs.lati)
    plt.title(title, fontsize=fontsize+4, pad=10)
    plt.xlabel("Longtitude [$^{\circ}$ $W$]", fontsize=fontsize, labelpad=10)
    plt.ylabel('Latitude [$^{\circ}$ $N$]', fontsize=fontsize, labelpad=10)
    plt.legend(fontsize=fontsize)
