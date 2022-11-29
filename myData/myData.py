'''
Module for data handling, Physics 411

readMinuteData(filepath):
    Function to read in minute resolution data and return a pandas dataframe.
    Nan values are automatically filled in using a cubic interpolation method.

    Parameters:
        filepath (str): filepath to data file to read.


getStationInfo(station):
    Function to get a station's longtitude, latitude and elevation.
    returns dataframe of lat, long and elev.

    Parameters:
        station (str): name of station.
    Returns:
        Pandas dataframe of long, lat, and elev.


removeStationInfo(name):

    Function to remove a station from a DataFrame of all stations' location info.

    Returns: DataFrame of stations' info.

    Parameters:
        name (str): name of Station to be deleted.


'''



import numpy as np
import pandas as pd

# Minute Data Parameters
START = 736330.0     # start date
END = 738733.99931   # end date
N = 3461760          # number of data points

# Hour Data Parameters

# MAINPATH = 'Data/' # for testing
MAINPATH = "../../Data/"


FILEPATH =  MAINPATH + '{}'
MINUTE_FILEPATH = MAINPATH + 'UVicWeatherdata_Minute_2022/{}_Tp.dat'
STATION_LOCATION_FILEPATH = MAINPATH + 'AllStation_Location.txt'
TEMP_PATH_HR = MAINPATH + 'All_hourly_temperature_data_2022.dat'
PRESS_PATH_HR = MAINPATH +  'All_hourly_pressure_data_2022.dat'

def readCoastLine():
    '''
    Function to read in the coast line data.
    Parameters: None
    Returns:
        pd dataframe of longitude and latitude.
    '''
    VI_coast = pd.read_csv(FILEPATH.format('VI_Coast.dat'), sep='\s+', names=['long', 'lati'])
    return VI_coast


def readMinuteData(name):
    '''
    Function to read in minute resolution data and return a pandas dataframe.
    Parameters:
        filepath (str): name of station.
    Returns:
        pd dataframe of times, temperature and pressure
    '''
    # Creating Series for time
    times = np.linspace(START, END, N)
    times = pd.Series(times, name='times')

    data = pd.read_csv(MINUTE_FILEPATH.format(name), sep='\s+', skiprows=2, names=['temperature', 'pressure'])

    data = pd.concat([times, data], axis=1)
    return data


def readHourData(col_index):
    '''
    Function to read hour resolution data given a filepath.
    Parameters:
        col_index (int): index referring to which station used.
             0. Bowser.
             1. Cortes.
             2. Craigflower.
             3. Cumberland.
             4. HappyValley.
             5. JamesBay.
             6. Macaulay.
             7. Monterey.
             8. Phoenix.
             9. RVYC.
            10. Rogers.
            11. ShawniganLake.
            12. Strawberry.
            13. UVicSci.
            14. VIU.

    Returns:
        : pandas frame of data, (timestamp, temp, press)
    '''
    col_index += 1

    times = pd.read_csv(TEMP_PATH_HR, sep="\s+", usecols=[0], names=["times"], skiprows=3)
    temp = pd.read_csv(TEMP_PATH_HR, sep="\s+", usecols=[col_index], names=["temperature"], skiprows=3)
    press = pd.read_csv(PRESS_PATH_HR, sep="\s+", usecols=[col_index], names=["pressure"], skiprows=3)

    return pd.concat([times, temp, press], axis=1)


def getStationInfo(station=None):
    '''
    Function to get a station's longtitude, latitude and elevation.

    Parameters:
        station (str) Optional: name of station. default returns dataframe for all stations
    Returns:
        Pandas dataframe of long, lat, and elev.

    '''

    if not station:
        data = pd.read_csv(STATION_LOCATION_FILEPATH, sep='\s+',
                   names=['station', 'long', 'lati', 'elev'], skiprows=1)
        return data


    sl = pd.read_csv(STATION_LOCATION_FILEPATH, sep='\s+',
                     names=['station', 'long', 'lat', 'elev'], skiprows=1)

    ind = np.where(sl.station == station)[0][0]

    long = pd.Series(sl.long.iloc[ind], name='long')
    lat = pd.Series(sl.lat.iloc[ind], name='lati')
    elev = pd.Series(sl.elev.iloc[ind], name='elev')
    return pd.concat([long, lat, elev], axis=1)


def removeStation(name):
    '''
    Function to remove a station from a DataFrame of all stations' location info.

    Returns: DataFrame of stations' info.

    Parameters:
        name (str): name of Station to be deleted.
             0. Bowser.
             1. Cortes.
             2. Craigflower.
             3. Cumberland.
             4. HappyValley.
             5. JamesBay.
             6. Macaulay.
             7. Monterey.
             8. Phoenix.
             9. RVYC.
            10. Rogers.
            11. ShawniganLake.
            12. Strawberry.
            13. UVicSci.
            14. VIU.
    '''

    data = pd.read_csv(STATION_LOCATION_FILEPATH, sep='\s+',
                       names=['station', 'long', 'lati', 'elev'], skiprows=1)

    idx = np.where(data == name)[0][0]      # getting index.
    data = data.drop(index=idx)             # dropping station.
    data = data.reset_index(drop=True)      # reindexing dataframe.

    return data


# List of functions. 
function_list = [readCoastLine, readMinuteData, readHourData, getStationInfo, removeStation]
