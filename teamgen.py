from datetime import date
import psycopg2
import namegenerator

def generate(cursor, c: int, division_id: int, leader_ids: list, ids: list, gender: str, start_date: date) -> str:
    '''Generate the SQL command to insert a new team. Use update to insert junior or end_date'''

    retstr = "INSERT INTO team (team_id, division_id, leader_id, name, gender, start_date) VALUES "

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "

        # team_id
        cursor.execute("SELECT * FROM nextval('team_team_id_seq');")
        seq = cursor.fetchone()
        id = seq[0]
        ids.append(id)

        # add to SQL string
        retstr += '(' + str(id) + ',' + str(division_id) + ',' + str(leader_ids[i]) + ",'" + namegenerator.gen(separator=' ') + "','" + gender + "','" + str(start_date) + "')"
    
    retstr += ";"
    return retstr

def update(team_id: int, division_id: int = None, leader_id: int = None, junior_leader_id: int = None, gender: str = None, start_date: date = None, end_date: date = None):
    '''Generate the SQL command to update a row in team.'''

    retstr = "UPDATE team SET "

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
        c += 1
    if junior_leader_id is not None:
        if c > 0:
            retstr += ", "
        retstr += "junior_leader_id = " + str(junior_leader_id)
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

    return retstr