from datetime import date, time 
from datetime import timedelta as td
from random import randrange as rr
from essential_generators import DocumentGenerator

def gendate(startDate: date, endDate:date) -> date:
    '''Generate a date between startDate and endDate'''
    timeDiff = endDate - startDate
    dayDiff = timeDiff.days
    randNumOfDays = rr(dayDiff)
    return startDate + td(days=randNumOfDays)

def gensentence() -> str:
    '''Generate a sentence without any apostophes, so it can be used as a string in SQL'''
    gen = DocumentGenerator()
    while(True):
        sentence = gen.sentence()
        if "'" not in sentence:
            return sentence    