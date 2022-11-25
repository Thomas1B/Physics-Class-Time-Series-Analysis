'''
Module for custom satistic functions.

UniformRandom(a, b):
    Function to return a random number from a uniform distribution between (a, b).

StudentConfidenceInterval(DATA, CONFIDENCE=0.95, DOF=False):
    Function to calculate the confidence interval based on the student-t distribution.

CI_psd(NS, interval=0.95, boxcar=False):
    Function to calculate the confidence interval of a power spectral density (PSD)
    based on the chi-squared distribution.
    
    Parameters:
        NS: number of sub sections.
        interval: default 95%, confidence interval as decimal.
        boxcar: default False, bool var for if a boxcar method was used to calculate the PSD.
        
    Returns: 
        lower and upper bounds
'''


import numpy as np
from scipy import stats as sp_stats

def StudentConfidenceInterval(DATA, CONFIDENCE=0.95, DOF=False):
    '''
    Function to calculate the confidence interval based on the student-t distribution.
    
    Parameters: DATA - list/array of data, CONFIDENCE - desired confidence interval as a decimal (default: 95%),
                DOF - degrees of freedom (default: N-1).
    
    Returns: lower and upper bounds of the confidence interval 
             and the t-value, (lower, upper, t-value).
             
    '''
    m = np.mean(DATA)     # Sample mean.
    s = np.std(DATA)      # Sample standard deviation.
    
    if not DOF: # default
        DOF = len(DATA)-1     # Degrees of freedom.
    
    T_C = np.abs(sp_stats.t.ppf((1-CONFIDENCE)/2, DOF)) # t-value (aka t_critical)
    
    LOWER = m - T_C * (s / np.sqrt(len(DATA))) 
    UPPER =  m + T_C * (s / np.sqrt(len(DATA)))
    return LOWER, UPPER, T_C 


def CI_psd(NS, interval=0.95, boxcar=False):
    '''
    Function to calculate the confidence interval of a power spectral density (PSD)
    based on the chi-squared distribution.
    
    Parameters:
        NS: number of sub sections.
        interval: default 95%, confidence interval as decimal.
        boxcar: default False, bool var for if a boxcar method was used to calculate the PSD.
        
    Returns: 
        lower and upper bounds
    '''
    M = 2*NS-1 # number of subsections
    
    nu = (4/3)*M # degrees of freedom
    if boxcar:
        nu = 2*M

        
    l = nu/sp_stats.chi2.ppf(1 - (1-interval)/2, nu)
    h = nu/sp_stats.chi2.ppf((1 - interval)/2, nu)
    
    return l, h
    
    
def UniformRandom(a, b):
    '''
    Function to return a random number from a uniform distribution between (a, b)
    '''
    return sp_stats.uniform.rvs(loc=a, scale=b-a)