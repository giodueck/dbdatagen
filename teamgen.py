from datetime import date
import persongen as pg
import namegenerator

def generate(cursor, c: int, division_id: int, leader_ids: list, junior_leader_ids: list, ids: list, gender: str, start_date: date) -> str:
    '''Generate the SQL command to insert a new team. Use update to insert junior or end_date'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "INSERT INTO team (team_id, division_id, leader_id, junior_leader_id, name, gender, start_date) VALUES "
    lthstr = ""

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "

        # team_id
        execute("SELECT * FROM nextval('team_team_id_seq');")
        seq = fetchone()
        id = seq[0]
        ids.append(id)

        # add to SQL string
        retstr += '(' + str(id) + ',' + str(division_id) + ',' + str(leader_ids[i]) + ',' + str(junior_leader_ids[i]) + ",'" + namegenerator.gen(separator=' ') + "','" + gender + "','" + str(start_date) + "')"
        lthstr += pg.leaderJoinTeam(cursor, leader_ids[i], id, False, start_date)
        lthstr += pg.leaderJoinTeam(cursor, junior_leader_ids[i], id, True, start_date)

    retstr += ";"
    return retstr + lthstr

def update(cursor, team_id: int, division_id: int = None, leader_id: int = None, junior_leader_id: int = None, gender: str = None, start_date: date = None, end_date: date = None, _date: date = None):
    '''Generate the SQL command to update a row in team.'''

    retstr = "UPDATE team SET "
    aditionalqs = ""

    # if nothing gets updated
    if division_id is None and leader_id is None and junior_leader_id is None and gender is None and start_date is None and end_date is None:
        return ""

    # set
    c = 0;
    if division_id is not None:
        retstr += "division_id = " + str(division_id)
        c += 1
    if leader_id is not None:
        if c > 0:
            retstr += ", "
        retstr += "leader_id = " + str(leader_id)
        aditionalqs += replaceTeamLeader(cursor, team_id, leader_id, False, _date)
        c += 1
    if junior_leader_id is not None:
        if c > 0:
            retstr += ", "
        retstr += "junior_leader_id = " + str(junior_leader_id)
        aditionalqs += replaceTeamLeader(cursor, team_id, junior_leader_id, True, _date)
        c += 1
    if gender is not None:
        if c > 0:
            retstr += ", "
        retstr += "gender = '" + str(gender) + "'"
        c += 1
    if start_date is not None:
        if c > 0:
            retstr += ", "
        retstr += "start_date = '" + str(start_date) + "'"
        c += 1
    if end_date is not None:
        if c > 0:
            retstr += ", "
        retstr += "end_date = '" + str(end_date) + "'"
        c += 1
    
    # where
    retstr += " WHERE team_id = " + str(team_id) + ";"

    return aditionalqs + retstr

def replaceTeamLeader(cursor, tid: int, lid: int, is_junior: bool, replace_date: date) -> str:
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
        retstr += "UPDATE leader_team_history SET leave_date = '" + str(replace_date) + "' WHERE leave_date IS null AND leader_id = " + str(oldlid) + ';'
    
    # new leader joins
    retstr += pg.leaderJoinTeam(cursor, lid, tid, is_junior, replace_date)
    
    # team gets updated
    if not is_junior:
        retstr += "UPDATE team SET leader_id = " + str(lid) + " WHERE team_id = %s;" % str(tid)
    else:
        retstr += "UPDATE team SET junior_leader_id = " + str(lid) + " WHERE team_id = %s;" % str(tid)
    return retstr