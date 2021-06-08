from datetime import date
import persongen as pg
import namegenerator

def generate(cursor, c: int, id_ctr: int, leader_team_history_id_ctr: int, division_id: int, leader_ids: list, junior_leader_ids: list, ids: list, gender: str, start_date: date) -> str:
    '''Generate the SQL command to insert a new team. Use update to insert junior or end_date'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "INSERT INTO team (team_id, division_id, leader_id, junior_leader_id, name, gender, start_date) VALUES "
    lthstr = ""

    for i in range(c):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])

        # team_id
        # execute("SELECT * FROM nextval('team_team_id_seq');")
        # seq = fetchone()
        # id = seq[0]
        ids.append(id_ctr)

        # add to SQL string
        retstr += "(%s,%s,%s,%s,'%s','%s','%s')" % (str(id_ctr), str(division_id), str(leader_ids[i]), str(junior_leader_ids[i]), namegenerator.gen(separator=' '), gender, str(start_date))
        sql, leader_team_history_id_ctr = pg.leaderJoinTeam(cursor, leader_team_history_id_ctr, leader_ids[i], id_ctr, False, start_date)
        lthstr = "".join([lthstr, sql])
        sql, leader_team_history_id_ctr = pg.leaderJoinTeam(cursor, leader_team_history_id_ctr, junior_leader_ids[i], id_ctr, True, start_date)
        lthstr = "".join([lthstr, sql])

        id_ctr += 1

    return ";".join([retstr, lthstr]), id_ctr, leader_team_history_id_ctr

def update(cursor, team_id: int, team_history_id_ctr: int, division_id: int = None, leader_id: int = None, junior_leader_id: int = None, gender: str = None, start_date: date = None, end_date: date = None, _date: date = None):
    '''Generate the SQL command to update a row in team.'''

    retstr = "UPDATE team SET "
    aditionalqs = ""

    # if nothing gets updated
    if division_id is None and leader_id is None and junior_leader_id is None and gender is None and start_date is None and end_date is None:
        return ""

    # set
    c = 0;
    if division_id is not None:
        string = "division_id = %s" % (str(division_id))
        retstr = "".join([retstr, string])
        c += 1
    if leader_id is not None:
        if c > 0:
            retstr = "".join([retstr, ", "])
        string = "leader_id = %s" % (str(leader_id))
        retstr = "".join([retstr, string])
        sql, team_history_id_ctr = replaceTeamLeader(cursor, team_history_id_ctr, team_id, leader_id, False, _date)
        aditionalqs = "".join([aditionalqs, sql])
        c += 1
    if junior_leader_id is not None:
        if c > 0:
            retstr = "".join([retstr, ", "])
        string = "junior_leader_id = %s" % (str(junior_leader_id))
        retstr = "".join([retstr, string])
        sql, team_history_id_ctr = replaceTeamLeader(cursor, team_history_id_ctr, team_id, junior_leader_id, True, _date)
        aditionalqs = "".join([aditionalqs, sql])
        c += 1
    if gender is not None:
        if c > 0:
            retstr = "".join([retstr, ", "])
        string = "gender = '%s'" % (str(gender))
        retstr = "".join([retstr, string])
        c += 1
    if start_date is not None:
        if c > 0:
            retstr = "".join([retstr, ", "])
        string = "start_date = '%s'" % (str(start_date))
        retstr = "".join([retstr, string])
        c += 1
    if end_date is not None:
        if c > 0:
            retstr = "".join([retstr, ", "])
        string = "end_date = '%s'" % (str(end_date))
        retstr = "".join([retstr, string])
        c += 1
    
    # where
    string = " WHERE team_id = %s;" % (str(team_id))
    retstr = "".join([retstr, string])

    return "".join([aditionalqs, retstr]), team_history_id_ctr

def replaceTeamLeader(cursor, team_history_id_ctr: int, tid: int, lid: int, is_junior: bool, replace_date: date) -> str:
    '''Generate the SQL command to update leader_team_history for an active leader.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    # get old leader
    if not is_junior:
        execute("SELECT leader_id FROM team WHERE team_id = %s;" % str(tid))
        oldlid = fetchone()[0]
    else:
        execute("SELECT junior_leader_id FROM team WHERE team_id = %s;" % str(tid))
        oldlid = fetchone()[0]
    
    retstr = ""
    # old leader leaves
    if oldlid is not None:
        retstr = "".join([retstr, "UPDATE leader_team_history SET leave_date = '%s' WHERE leave_date IS null AND leader_id = %s;" % (str(replace_date), str(oldlid))])
    
    # new leader joins
    sql, team_history_id_ctr = pg.leaderJoinTeam(cursor, team_history_id_ctr, lid, tid, is_junior, replace_date)
    retstr = "".join([retstr, sql])
    
    # team gets updated
    if not is_junior:
        retstr = "".join([retstr, "UPDATE team SET leader_id = %s WHERE team_id = %s;" % (str(tid), str(lid))])
    else:
        retstr = "".join([retstr, "UPDATE team SET junior_leader_id = %s WHERE team_id = %s;" % (str(tid), str(lid))])
    return retstr, team_history_id_ctr