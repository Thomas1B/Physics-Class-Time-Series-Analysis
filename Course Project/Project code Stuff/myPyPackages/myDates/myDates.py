'''
For Physics 411, Time Series Analysis.
Module for convert dates from a string to a number or a number to a string.

Similar to Matlab's datenum and datestr functions.

DateStrtoNum(datestr, dtype)

DateNumtoStr(datenum, dtype, giveTime=False)

NumToStr(datenum, giveTime = False)
'''


import numpy as np
from datetime import datetime
from scipy import stats as sp_stats

#  Date handling Function
def DateStrtoNum(datestr, dtype):
    '''
    Function to convert a date number to a date string.
    Takes in a number representing the date.
    Returns the date in a string.

    Default returns: 'day/month/year'
    if giveTime = True, returns: 'day/month/year, hrs:mins'
    '''
    T0 = datetime.toordinal(datetime(2016, 1, 1)) + 365 # constant

    d = datestr.split(',')
    day, month, year = d[0].split('/')

    if (dtype == 'min'):
        if (len(d) > 1):
            hr, minn = d[1].split(':')
            datenum = datetime.toordinal(datetime(int(year), int(month), int(day))) + 366 +  (int(hr)/24) + (int(minn)/(24*60))
            return datenum
        else:
            datenum = datetime.toordinal(datetime(int(year), int(month), int(day))) + 366
            return datenum
    elif (dtype == 'hr'):
        if (len(d) > 1):
            hr, minn = d[1].split(':')
            return datetime.toordinal(datetime(int(year), int(month), int(day))) + 365 + (int(hr)/24) + (int(minn)/(24*60)) - T0
        else:
            return datetime.toordinal(datetime(int(year), int(month), int(day))) + 365 - T0

def NumToStr(datenum, giveTime = False):
    '''
    Function to convert a date number to a date string.
    Takes in a number representing the date.
    Returns the date in a string.

    Default returns: 'day/month/year'
    if giveTime = True, returns: 'day/month/year, hrs:mins'
    '''
    ds = datetime.fromordinal(1)
    days = -1
    if (datenum > 0):
        days = datenum - 366
    if days > 0:
        ds = datetime.fromordinal(int(days))
    hours = (datenum % 1) * 24
    mins = (hours - int(hours))*60

    if (round(mins) >= 60):
        hours += 1
        mins = (mins - 60)

    if (giveTime):
        return ds.strftime("{}/{}/{}, {:02d}:{:02d}".format(ds.day, ds.month, ds.year, int(hours), round(mins)))

    return ds.strftime("{}/{}/{}".format(ds.day, ds.month, ds.year))

def DateNumtoStr(datenum, dtype, giveTime=False):
    '''
    Function to convert timestamps into a date string format.

    datenum: date number
    dtype: data type; mn - minute, hr - hour
    giveTime: True/False, gives clock time.

    returns a date format string.
    '''
    if (dtype == 'hr'):
        startDate = datetime.toordinal(datetime(2016, 1, 1)) + 366.
        return NumToStr(startDate + int(datenum) + (datenum%1) , giveTime)
    elif (dtype == "min"):
        return NumToStr(datenum, giveTime)

def getRange(data, start, end):
    '''
    Function to return a certain range of data.

    Parameters:
        Data: DataFrame of data.
        start (float): start date of range.
        end (float): end date of range.
            See myDates.DateStrtoNum()

    Returns:
        DataFrame.
    '''
    tmp = data[data.times >= start]
    return tmp[tmp.times < end]



# List of functions. 
function_list = [DateStrtoNum, NumToStr, DateNumtoStr, getRange]