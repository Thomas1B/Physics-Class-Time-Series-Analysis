'''
Module for Custom Signal Processing Functions.

def applyGrid(data, stationInfo, grid, method=''):
    Function to apply a scipy griddata and interpolation for making a heatmap.
    Returns: (tuple): (xi, yi, zi, coastline, locs)

GetNS_NFFT(data):
    Function to determine the best NS and NFFT for calculating the power spectral density (PSD).
    returns NS, NFFT.

PowerSpectrum(data, dt, rec_len):
    Function to calculate the power spectrum density (PSD) of a time series
    using the Fast Fourier Transform (fft) package from scipy.
'''

import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq, fftshift
from .myData import readCoastLine
from scipy import interpolate



def applyGridInterp(data, stationInfo, grid, method=''):
    '''
    Function to apply a scipy griddata and interpolation for making a heatmap.

    Parameters:
        data: data to be analized.
        StationInfo (DataFrame): dataframe of stations' info.
        grid (tuple): grid cells (x, y)-axis.
        method (str): method to use for the intepolation, default = cubic.

    Returns: (tuple): (xi, yi, zi, coastline, locs)
        xi & yi: arrays representing the coordinates of a grid.
        coastline: DataFrame for the coastline.
        locs: DataFrame for station locations.

    '''
    coastline = readCoastLine() # getting coastal line.

    # Getting min and max for long and lati for gridding.
    min_long, min_lat = coastline.min()
    max_long, max_lat = coastline.max()

    # Creating grids for gridding data.
    xi = np.linspace(min_long, max_long, int(grid[0]))
    yi = np.linspace(min_lat, max_lat, int(grid[1]))
    xi, yi = np.meshgrid(xi, yi)

    if method == '':
        method = 'cubic'

    locs = pd.concat([stationInfo.long, stationInfo.lati], axis=1)

    # Doing the interpolation.
    zi = interpolate.griddata(locs, data, (xi, yi), method=method)
    return xi, yi, zi, coastline, locs

def GetNS_NFFT(data, showInfo=False):
    '''
    Function to determine the best NS and NFFT for calculating the power spectral density (PSD).
    returns NS, NFFT.

    N: total record length (data points)
    NS: Number of sub sections (>= 8)
    NFFT: length of subsection (powers of 2)
    '''
    # Determing best NS, NFFT for sub-sampling
    NS = []
    NFFT = []
    N = len(data)
    for i in range(3,20):
        for j in range(8, 30):
            if (j*(2**i) < N):
                NS.append(j)      # number of sections
                NFFT.append(2**i) # number of pts per sec

    NS = NS[-1]      # number of subsection
    NFFT = NFFT[-1]  # number of points per section

    if showInfo:
        print("NS*NFFT = NT < N")
        print(f"{NS}*{NFFT} = {NS*NFFT} < {N}")
        print("NFFT = 2^{:.0f} = {}".format(np.log2(NFFT), NFFT))

    return NS, NFFT


def PowerSpectrum(data, dt, rec_len):
    '''
    Function to calculate the power spectrum density (PSD) of a time series
    using the Fast Fourier Transform (fft) package from scipy.

    Parameters:
        data [1D list/array]: y-values of time series.
        dt (delta t) [float]: sample rate.
        rec_len [float]: record length of time series.

    Returns:
        Power spectrum density [array]: array of the calculated PSD.
        Frequency points [array]: array of frquencies associated with the PSD.

    '''
    xs = np.arange(0, rec_len, dt)
    N = len(xs)

    FT = fft(data)[:N//2]
    freqs = fftfreq(N, dt)[:N//2]

    PSD = np.abs(FT**2)/N

    return PSD, freqs
