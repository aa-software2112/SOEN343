"""This module contains general helper functions."""
import time

def convertEpochToDatetime(epoch_time):
    """Returns time in 'month/day/year hour:minute:second' format given the epoch time"""
    return time.strftime("%m/%d/%Y %H:%M:%S %Z", time.localtime(epoch_time))

    
