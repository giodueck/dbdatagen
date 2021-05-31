from datetime import date, time 
from datetime import timedelta as td
from random import randrange as rr

def gendate(startDate: date, endDate:date) -> date:
    '''Generate a date between startDate and endDate'''
    timeDiff = endDate - startDate
    dayDiff = timeDiff.days
    randNumOfDays = rr(dayDiff)
    return startDate + td(days=randNumOfDays)