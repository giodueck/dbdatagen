from datetime import date
from random import randrange as rr
import names
import miscgen

def generate(cursor, c: int, minBirthday: date, maxBirthday: date, ids: list, gender: str = None) -> str:
    '''Generate the SQL command to insert c amount of persons.
        cursor: cursor to execute sequence operations
        c: count, number of rows to generate
        minBirthday, maxBirthday: lower and upper bound of possible birthdays for date_of_birth
        ids: list to store the generated person_ids in
        gender: string that holds gender ("M" or "F")'''
    
    # sql format is
    # "INSERT INTO person (person_id, first_name, last_name, date_of_birth, gender)
    #      VALUES (id1, fn1, ln1, d1, g1),
    #             .
    #             .
    #             (idc-1, fnc-1, lnc-1, dc-1, gc-1);"

    retstr = "INSERT INTO person (person_id, first_name, last_name, date_of_birth, gender) VALUES "
    
    og = gender

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "

        # person_id
        cursor.execute("SELECT * FROM nextval('person_person_id_seq');")
        seq = cursor.fetchone()
        id = seq[0]
        ids.append(id)

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
        dob = miscgen.gendate(minBirthday, maxBirthday)

        # add to SQL string
        retstr += "('" + str(id) + "','" + fn + "','" + ln + "','" + str(dob) + "','" + gender + "')"

        # reset gender if None
        gender = og
    
    retstr += ";"

    return retstr

def leadergen(cursor, c: int, person_ids: list, is_junior: bool, ids: list, historyids: list, start_date: date) -> str:
    '''Generate the SQL command to make the person person_id a leader.'''

    # sql format is
    # "INSERT INTO leader (leader_id, person_id, is_junior)
    #      VALUES (int, bool);"

    retstr = "INSERT INTO leader (leader_id, person_id, is_junior) VALUES "
    historystr = "INSERT INTO leader_history (leader_history_id, person_id, start_date, is_junior) VALUES "

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "
            historystr += ", "
        
        # leader_id
        cursor.execute("SELECT * FROM nextval('leader_leader_id_seq_1_1');")
        seq = cursor.fetchone()
        id = seq[0]
        ids.append(id)

        # leader_history_id
        cursor.execute("SELECT * FROM nextval('leader_history_leader_history_id_seq');")
        seq = cursor.fetchone()
        hid = seq[0]
        historyids.append(hid)

        # add to SQL strings
        retstr += "(" + str(id) + "," + str(person_ids[i]) + "," + str(is_junior) + ")"
        historystr += "(" + str(hid) + "," + str(person_ids[i]) + ",'" + str(start_date) + "'," + str(is_junior) + ")"

    retstr += "; "
    historystr += ";"

    return retstr + historystr

def scoutgen(cursor, c: int, person_ids: list, ids: list, historyids: list, start_date: date, team_id: int = None, team_join_date: date = None, thistoryids: list = None) -> str:
    '''Generate the SQL command to make the person person_id a scout.'''

    # sql format is
    # "INSERT INTO scout (scout_id, person_id, team_id)
    #      VALUES (int, int);"

    retstr = "INSERT INTO scout (scout_id, person_id, team_id) VALUES "
    historystr = "INSERT INTO scout_history (scout_history_id, person_id, start_date) VALUES "
    thistorystr = " INSERT INTO scout_team_history (scout_team_history_id, team_id, scout_id, join_date) VALUES "

    if team_id is None:
        team_id = 'null'

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "
            historystr += ", "
            if team_id != 'null':
                thistorystr += ", "
        
        # scout_id
        cursor.execute("SELECT * FROM nextval('scout_scout_id_seq');")
        seq = cursor.fetchone()
        id = seq[0]
        ids.append(id)

        # scout_history_id
        cursor.execute("SELECT * FROM nextval('scout_history_scout_history_id_seq');")
        seq = cursor.fetchone()
        hid = seq[0]
        historyids.append(hid)

        # scout_team_history_id
        if team_id != 'null':
            cursor.execute("SELECT * FROM nextval('scout_team_history_scout_team_history_id_seq');")
            seq = cursor.fetchone()
            thid = seq[0]
            thistoryids.append(thid)

        # add to SQL string
        retstr += "(" + str(id) + "," + str(person_ids[i]) + "," + str(team_id) + ")"
        historystr += "(" + str(hid) + "," + str(person_ids[i]) + ",'" + str(start_date) + "')"
        if team_id != 'null':
            thistorystr += "(" + str(thid) + "," + str(team_id) + ',' + str(id) + ",'" + str(team_join_date) + "')"

    retstr += "; "
    historystr += ";"
    if team_id != 'null':
        thistorystr += ";"
        historystr += thistorystr

    return retstr + historystr

def leaderLeave(pid: int, end_date: date) -> str:
    '''Generate the SQL command to update leader_history for an active leader.'''

    return  "UPDATE leader_history SET end_date = '" + str(end_date) + "' WHERE end_date IS null AND person_id = " + str(pid) + ';'

def scoutLeave(pid: int, end_date: date) -> str:
    '''Generate the SQL command to update scout_history for an active scout.'''

    return  "UPDATE scout_history SET end_date = '" + str(end_date) + "' WHERE end_date IS null AND person_id = " + str(pid) + ';'

def leaderRejoin(cursor, person_id: int, is_junior: bool, historyids: list, start_date: date) -> str:
    '''Generate the SQL command to update leader_history for an inactive leader.'''

    historystr = "INSERT INTO leader_history (leader_history_id, person_id, start_date, is_junior) VALUES "

    # leader_history_id
    cursor.execute("SELECT * FROM nextval('leader_history_leader_history_id_seq');")
    seq = cursor.fetchone()
    hid = seq[0]
    historyids.append(hid)

    historystr += "(" + str(hid) + "," + str(person_id) + ",'" + str(start_date) + "'," + str(is_junior) + ");"

    return historystr

def scoutRejoin(cursor, person_id: int, historyids: list, start_date: date) -> str:
    '''Generate the SQL command to update scout_history for an inactive scout.'''

    historystr = "INSERT INTO scout_history (scout_history_id, person_id, start_date) VALUES "

    # scout_history_id
    cursor.execute("SELECT * FROM nextval('scout_history_scout_history_id_seq');")
    seq = cursor.fetchone()
    hid = seq[0]
    historyids.append(hid)

    historystr += "(" + str(hid) + "," + str(person_id) + ",'" + str(start_date) + "');"

    return historystr