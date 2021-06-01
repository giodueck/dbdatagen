from datetime import date
from random import randrange as rr

import names
from miscgen import gendate

def generate(c: int, minBirthday: date, maxBirthday: date, gender: str = None) -> str:
    '''Generate the SQL command to insert c amount of persons.
        c: count, number of rows to generate
        minBirthday, maxBirthday: lower and upper bound of possible birthdays for date_of_birth
        gender: string that holds gender ("M" or "F")'''
    
    # sql format is
    # "INSERT INTO person (first_name, last_name, date_of_birth, gender)
    #      VALUES (fn1, ln1, d1, g1),
    #             .
    #             .
    #             (fnc-1, lnc-1, dc-1, gc-1);"

    retstr = "INSERT INTO person (first_name, last_name, date_of_birth, gender) VALUES "
    
    og = gender

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "

        # first_name
        if gender == 'M' or gender == 'm':
            fn = names.get_first_name("male")
        elif gender == 'F' or gender == 'f':
            fn = names.get_first_name("female")
        else:
            rand = rr(2)
            if rand == 0:
                gender = "M"
                fn = names.get_first_name("male")
            else:
                gender = "F"
                fn = names.get_first_name("female")
        
        # last_name
        ln = names.get_last_name()

        # date_of_birth
        dob = gendate(minBirthday, maxBirthday)

        # add to SQL string
        retstr += '(' + fn + ',' + ln + ',' + str(dob) + ',' + gender + ')'

        # reset gender if None
        gender = og
    
    retstr += ";"

    return retstr

def leadergen(person_id: int, is_junior: bool) -> str:
    '''Generate the SQL command to make the person person_id a leader.'''

    # sql format is
    # "INSERT INTO leader (person_id, is_junior)
    #      VALUES (int, bool);"

    return "INSERT INTO leader (person_id, is_junior) VALUES (" + str(person_id) + ',' + str(is_junior) + ");"

def scoutgen(person_id: int, team_id: int) -> str:
    '''Generate the SQL command to make the person person_id a scout.'''

    # sql format is
    # "INSERT INTO scout (person_id, team_id)
    #      VALUES (int, int);"

    return "INSERT INTO scout (person_id, team_id) VALUES (" + str(person_id) + ',' + str(team_id) + ");"