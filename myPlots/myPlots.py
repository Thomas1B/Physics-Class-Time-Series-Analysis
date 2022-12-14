'''
Module for handling custom plotting functions


'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate


# from myData import getStationInfo # For testing
from ..myData import getStationInfo


def plotLocalHeatMap(stuff,
                 title='',
                 barFormat='%.1f',
                 style='pcolor',
                 fontsize=12,
                 axisLimits=False):
    '''
    Function to plot a heat map after apply a scipy griddata.

    Parameters:
        data (tuple): (xi, yi, zi, coastline, locs) *see applyGrid()
        useUnit (T/P): T for temperature units, P for pressure units.
        title (str): title of map.
        style (str): style used for coloring map (pcolor, contourf) default pcolor.
        fontsize (int): fontsize to use for labels default 12.
        axisLimits (bool): to apply axis limits on the plot, default False.
    '''
    xi, yi, zi, VI_coast, stations = stuff
    

    # Creating the Heatmap
    ax = plt.axes()
    ax.set_facecolor('steelblue') # coloring ocean.

    plt.plot(VI_coast.long, VI_coast.lati, color="k", linewidth=1) # plotting land
    plt.fill(VI_coast.long, VI_coast.lati, zorder=0, color="olivedrab") # coloring land


    # Coloring heat map
    cmap = plt.get_cmap('jet')
    c = ''
    if  style == 'contourf':
        c = plt.contourf(xi, yi, zi, 16, cmap=cmap)
        plt.contour(xi, yi, zi, 15, colors='k', linewidths=0.5, alpha=0.5)

    else:
        c = plt.pcolor(xi, yi, zi, cmap=cmap)
        plt.rcParams['pcolor.shading'] = 'auto'


    cbar = plt.colorbar(c, format=barFormat, pad=0.02) # adding a color bar.
    # plotting station locations.
    plt.scatter(stations.long,
                stations.lati, 
                color='white',
                edgecolor='r', 
                label='Station',
                s=50,
                zorder=10)  


    # limits for plot
    if axisLimits:
        station_info = getStationInfo()
        maxs = station_info.max()[1:3] + 0.05
        mins = station_info.min()[1:3] - 0.05
        plt.xlim(mins.long)
        plt.ylim(mins.lati, maxs.lati)

    plt.title(title, fontsize=fontsize+4, pad=15)
    plt.xlabel("Longtitude [$^{\circ}$ $W$]", fontsize=fontsize, labelpad=10)
    plt.ylabel('Latitude [$^{\circ}$ $N$]', fontsize=fontsize, labelpad=10)
    plt.legend(fontsize=fontsize)
    
    plt.tick_params(labelsize=fontsize-2)
    cbar.ax.tick_params(labelsize=fontsize-2)



def plotGlobalHeatMap(stuff, 
                 title='',
                 barFormat='%.1f',
                 style='pcolor',
                 fontsize=12,
                 axisLimits=False):

    xi, yi, temps, coastline, locations = stuff

    ax = plt.axes()
    ax.set_facecolor('steelblue') # coloring ocean.

    plt.plot(coastline.long, coastline.lati, color="k", linewidth=0.5) # plotting land
    plt.fill(coastline.long, coastline.lati, zorder=0, color="olivedrab") # coloring land

    # Coloring heat map
    cmap = plt.get_cmap('jet')
    c = ''
    if  style == 'contourf':
        c = plt.contourf(xi, yi, zi, 16, cmap=cmap)
        plt.contour(xi, yi, zi, 15, colors='k', linewidths=0.5, alpha=0.5)

    else:
        c = plt.pcolor(xi, yi, zi, cmap=cmap)
        plt.rcParams['pcolor.shading'] = 'auto'

    fontsize=12
    plt.scatter(locations.long, 
                locations.lati,
                color='white',
                edgecolor='r',
                label="Station")  # plotting station locations.
    plt.title(title, fontsize=fontsize+4, pad=10)
    plt.xlabel("Longtitude [$^{\circ}$ $W$]", fontsize=fontsize, labelpad=10)
    plt.ylabel('Latitude [$^{\circ}$ $N$]', fontsize=fontsize, labelpad=10)
    plt.legend(fontsize=fontsize)
    
    if axisLimits:
        maxs = station_info.max()[1:3] + 0.05
        mins = station_info.min()[1:3] - 0.05
        plt.xlim(mins.long)
        plt.ylim(mins.lati, maxs.lati)

    plt.title(title, fontsize=fontsize+4, pad=15)
    plt.xlabel("Longtitude [$^{\circ}$ $W$]", fontsize=fontsize, labelpad=10)
    plt.ylabel('Latitude [$^{\circ}$ $N$]', fontsize=fontsize, labelpad=10)
    plt.legend(fontsize=fontsize)
    
    plt.tick_params(labelsize=fontsize-2)
    cbar.ax.tick_params(labelsize=fontsize-2)

# List of functions. 
function_list = [plotLocalHeatMap, plotGlobalHeatMap]