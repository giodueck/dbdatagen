from datetime import date
from random import randrange as rr
from datetime import timedelta
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

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "INSERT INTO person (person_id, first_name, last_name, date_of_birth, gender) VALUES "
    
    og = gender

    for i in range(c):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])

        # person_id
        execute("SELECT * FROM nextval('person_person_id_seq');")
        seq = fetchone()
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
        # sql += "('" + str(id) + "','" + fn + "','" + ln + "','" + str(dob) + "','" + gender + "')"
        sql = "(%s,'%s','%s','%s','%s')" % (str(id), fn, ln, str(dob), gender)
        retstr = "".join([retstr, sql])

        # reset gender if None
        gender = og
    
    retstr = "".join([retstr, ";"])

    return retstr

def leadergen(cursor, c: int, person_ids: list, is_junior: bool, ids: list, start_date: date) -> str:
    '''Generate the SQL command to make the person person_id a leader.'''

    # sql format is
    # "INSERT INTO leader (leader_id, person_id, is_junior)
    #      VALUES (int, bool);"

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "INSERT INTO leader (leader_id, person_id, is_junior) VALUES "
    historystr = "INSERT INTO leader_history (leader_history_id, person_id, start_date, is_junior) VALUES "

    for i in range(c):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])
            historystr = "".join([historystr, ", "])
        
        # leader_id
        execute("SELECT * FROM nextval('leader_leader_id_seq_1_1');")
        seq = fetchone()
        id = seq[0]
        ids.append(id)

        # leader_history_id
        execute("SELECT * FROM nextval('leader_history_leader_history_id_seq');")
        seq = fetchone()
        hid = seq[0]

        # add to SQL strings
        # sql += "(" + str(id) + "," + str(person_ids[i]) + "," + str(is_junior) + ")"
        sql = "(%s,%s,%s)" % (str(id), str(person_ids[i]), str(is_junior))
        retstr = "".join([retstr, sql])
        # hsql += "(" + str(hid) + "," + str(person_ids[i]) + ",'" + str(start_date) + "'," + str(is_junior) + ")"
        hsql = "(%s,%s,'%s',%s)" % (str(hid), str(person_ids[i]), str(start_date), str(is_junior))
        historystr = "".join([historystr, hsql])

    retstr = "".join([retstr, "; "])
    historystr = "".join([historystr, ";"])

    return "".join([retstr, historystr])

def scoutgen(cursor, c: int, person_ids: list, ids: list, start_date: date, team_id: int = None, team_join_date: date = None) -> str:
    '''Generate the SQL command to make the person person_id a scout.'''

    # sql format is
    # "INSERT INTO scout (scout_id, person_id, team_id)
    #      VALUES (int, int);"

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "INSERT INTO scout (scout_id, person_id, team_id) VALUES "
    historystr = "INSERT INTO scout_history (scout_history_id, person_id, start_date) VALUES "
    thistorystr = " INSERT INTO scout_team_history (scout_team_history_id, team_id, scout_id, join_date) VALUES "

    if team_id is None:
        team_id = 'null'

    for i in range(c):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])
            historystr = "".join([historystr, ", "])
            if team_id != 'null':
                thistorystr = "".join([thistorystr, ", "])
        
        # scout_id
        execute("SELECT * FROM nextval('scout_scout_id_seq');")
        seq = fetchone()
        id = seq[0]
        ids.append(id)

        # scout_history_id
        execute("SELECT * FROM nextval('scout_history_scout_history_id_seq');")
        seq = fetchone()
        hid = seq[0]

        # scout_team_history_id
        if team_id != 'null':
            execute("SELECT * FROM nextval('scout_team_history_scout_team_history_id_seq');")
            seq = fetchone()
            thid = seq[0]

        # add to SQL string
        # sql += "(" + str(id) + "," + str(person_ids[i]) + "," + str(team_id) + ")"
        sql = "(%s,%s,%s)" % (str(id), str(person_ids[i]), str(team_id))
        retstr = "".join([retstr, sql])
        # hsql += "(" + str(hid) + "," + str(person_ids[i]) + ",'" + str(start_date) + "')"
        hsql = "(%s,%s,'%s')" % (str(hid), str(person_ids[i]), str(start_date))
        historystr = "".join([historystr, hsql])
        if team_id != 'null':
            # thsql += "(" + str(thid) + "," + str(team_id) + ',' + str(id) + ",'" + str(team_join_date) + "')"
            thsql = "(%s,%s,%s,'%s')" % (str(thid), str(team_id), str(id), str(team_join_date))
            thistorystr = "".join([thistorystr, thsql])

    retstr = "".join([retstr, "; "])
    historystr = "".join([historystr, ";"])
    if team_id != 'null':
        historystr = "; ".join([historystr, thistorystr])

    return "".join([retstr, historystr])

def leaderLeave(pid: int, end_date: date) -> str:
    '''Generate the SQL command to update leader_history for an active leader.'''

    return  "UPDATE leader_history SET end_date = '%s' WHERE end_date IS null AND person_id = %s;" % (str(end_date), str(pid))

def scoutLeave(cursor, pid: int, end_date: date) -> str:
    '''Generate the SQL command to update scout_history for an active scout.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "UPDATE scout_history SET end_date = '%s' WHERE end_date IS null AND person_id = %s;" % (str(end_date), str(pid))
    
    # leave team too
    execute("SELECT team_id, scout_id FROM scout WHERE person_id = %s;" % str(pid))
    scout = cursor.fetchone()
    if scout[0] is not None:
        retstr = "".join([retstr, scoutLeaveTeam(scout[1], end_date)])
    
    return retstr

def leaderRejoin(cursor, pid: int, is_junior: bool, start_date: date) -> str:
    '''Generate the SQL command to update leader_history for an inactive leader.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    historystr = "INSERT INTO leader_history (leader_history_id, person_id, start_date, is_junior) VALUES "

    # leader_history_id
    execute("SELECT * FROM nextval('leader_history_leader_history_id_seq');")
    seq = fetchone()
    hid = seq[0]

    sql = "(%s,%s,'%s',%s);" % (str(hid), str(pid), str(start_date), str(is_junior))
    return "".join([historystr, sql])

def scoutRejoin(cursor, pid: int, start_date: date, team_id: int = None, team_join_date: date = None) -> str:
    '''Generate the SQL command to update scout_history for an inactive scout.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    historystr = "INSERT INTO scout_history (scout_history_id, person_id, start_date) VALUES "

    # scout_history_id
    execute("SELECT * FROM nextval('scout_history_scout_history_id_seq');")
    seq = fetchone()
    hid = seq[0]

    sql = "(%s,%s,'%s');" % (str(hid), str(pid), str(start_date))
    historystr = "".join([historystr, sql])

    # rejoin team too
    execute("SELECT team_id, scout_id FROM scout WHERE person_id = %s;" % str(pid))
    scout = cursor.fetchone()
    if team_id is not None:
        historystr = "".join([historystr, scoutJoinTeam(cursor, scout[1], team_id, team_join_date)])
    
    return historystr

def scoutLeaveTeam(sid: int, leave_date: date) -> str:
    '''Generate the SQL command to update scout_team_history for an active scout.'''

    retstr = "UPDATE scout_team_history SET leave_date = '%s' WHERE leave_date IS null AND scout_id = %s;" % (str(leave_date), str(sid))
    retstr = "".join([retstr, "UPDATE scout SET team_id = null WHERE scout_id = %s;" % str(sid)])
    return retstr

def scoutJoinTeam(cursor, sid: int, tid: int, join_date: date) -> str:
    '''Generate the SQL command to update scout_team_history for an active scout.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    thistorystr = " INSERT INTO scout_team_history (scout_team_history_id, team_id, scout_id, join_date) VALUES "

    # scout_team_history_id
    execute("SELECT * FROM nextval('scout_team_history_scout_team_history_id_seq');")
    seq = fetchone()
    sthid = seq[0]

    sql = "(%s,%s,%s,'%s');" % (str(sthid), str(tid), str(sid), str(join_date))
    return "".join([thistorystr, sql])

def leaderJoinTeam(cursor, lid: int, tid: int, is_junior: bool, join_date: date) -> str:
    '''Generate the SQL command to update leader_team_history for an active leader.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    thistorystr = " INSERT INTO leader_team_history (leader_team_history_id, team_id, leader_id, is_junior, join_date) VALUES "

    # leader_team_history_id
    execute("SELECT * FROM nextval('leader_team_history_leader_team_history_id_seq');")
    seq = fetchone()
    lthid = seq[0]

    sql = "(%s,%s,%s,%s,'%s');" % (str(lthid), str(tid), str(lid), str(is_junior), str(join_date))
    return "".join([thistorystr, sql])

def scoutPause(cursor, pid: int, minDate: date, maxDate: date, tid: int) -> str:
    '''Generates the SQL commands to update scout_history and simulate a scout exiting and reentering the programme.'''

    pauseDate = miscgen.gendate(minDate, maxDate)

    retstr = scoutLeave(cursor, pid, pauseDate)
    pauseDate.__add__(timedelta(days=30))
    retstr = "".join([retstr, scoutRejoin(cursor, pid, pauseDate, tid, pauseDate)])
    return retstr

def leaderPause(cursor, pid: int, minDate: date, maxDate: date, is_junior: bool) -> str:
    '''Generates the SQL commands to update leader_history and simulate a leader exiting and reentering the programme.'''

    pauseDate = miscgen.gendate(minDate, maxDate)

    retstr = leaderLeave(pid, pauseDate)
    pauseDate.__add__(timedelta(days=30))
    retstr = "".join([retstr, leaderRejoin(cursor, pid, is_junior, pauseDate)])
    return retstr