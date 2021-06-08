'''Data generator for a postgresql project for uni'''

import psycopg2
# https://www.psycopg.org/docs/usage.html
import persongen as pg
import entitygen as eg
import awardgen as ag
import teamgen as tg

import time
from datetime import date
import sys

def openConn():
    '''Opens a connection to the db. Returns (conn, cursor) tuple.'''

    # Connect to an existing database
    conn = psycopg2.connect(database="dgtopti", user="postgres", password=" ")

    # Open a cursor to perform db operations
    return conn, conn.cursor(), conn.cursor().execute

def closeConn(conn, cursor):
    '''Commits and closes connection to the db.'''

    # Commit
    conn.commit()

    # Close communication with the db
    cursor.close()
    conn.close()

def award(cursor, person_id: int, leader_id: int, i: int, category: int = None):
    '''Gives the person 1 or 2 awards depending on i'''

    execute = cursor.execute

    # define award-list
    if category is not None:
        auxAwards = awards[category]
        auxReqs = requirements[category]
    else:
        auxAwards = awards[3]
        auxReqs = requirements[3]

    if i % 2 == 0:
        auxAwards = [auxAwards[0], auxAwards[1]]
        execute(ag.giveRequirements(person_id, auxReqs[0], leader_id, startDate, today))
        execute(ag.giveRequirements(person_id, auxReqs[1], leader_id, startDate, today))
    else:
        auxAwards = [auxAwards[0]]
        execute(ag.giveRequirements(person_id, auxReqs[0], leader_id, startDate, today))

    execute(ag.giveAwards(person_id, auxAwards, leader_id, startDate, today))

# Numbers
nOffices = 40
nOutposts = 50  # * nOffices
nDivisions = 3  # * nOutposts * nOffices
nTeams = 10     # * nDivisions * nOutposts * nOffices
nScouts = 5     # * nTeams * nDivisions * nOutposts * nOffices
# Totals:
# Scouts = 40 * 50 * 3 * 10 * 5 = 300K
# Leaders = (40 + 40*50 + 40*50*3 + 40*50*3*10) *2 = 136 080
#       163 920 extra leaders will be generated to fill the 300K

nAwards = 2
nReqs = 2

# Lists to store created ids
offices = list()
outposts = list()
divisions = list()

categories = list()

awards = list()
requirements = list()

auxPersons = list()
auxLeaders = list()
auxViceLeaders = list()
auxScouts = list()
auxTeams = list()

# Useful variables
leaderMinBirthday = date(1970, 1, 1)
leaderMaxBirthday = date(2003, 12, 31)

discoveryMinBirthday = date(2010, 1, 1)
discoveryMaxBirthday = date(2012, 12, 31)

adventureMinBirthday = date(2007, 1, 1)
adventureMaxBirthday = date(2009, 12, 31)

expeditionMinBirthday = date(2004, 1, 1)
expeditionMaxBirthday = date(2006, 12, 31)

scoutMinBirthdays = [discoveryMinBirthday, adventureMinBirthday, expeditionMinBirthday]
scoutMaxBirthdays = [discoveryMaxBirthday, adventureMaxBirthday, expeditionMaxBirthday]

startDate = date(2019, 1, 1)
today = date(2021, 1, 1)

def generate():
    # ID counters
    award_id_ctr = 1
    req_id_ctr = 1

    office_id_ctr = 1
    outpost_id_ctr = 1
    division_id_ctr = 1

    person_id_ctr = 1
    leader_id_ctr = 1
    scout_id_ctr = 1
    scout_history_id_ctr = 1
    scout_team_history_id_ctr = 1
    leader_history_id_ctr = 1
    leader_team_history_id_ctr = 1

    team_id_ctr = 1

    # Awards & requirements
    for i in range(4):
        conn, cursor, execute = openConn()

        # Awards
        awards.append(list())
        try:
            sql, award_id_ctr = ag.generate(cursor, nAwards, award_id_ctr, awards[i], categories[i])
        except:
            # leader awards will cause an exception because of categories
            sql, award_id_ctr = ag.generate(cursor, nAwards, award_id_ctr, awards[i], None)
        execute(sql)

        # Requirements
        requirements.append(list())
        for j in range(len(awards[i])):
            requirements[i].append(list())
            sql, req_id_ctr = ag.requirementgen(cursor, nReqs, req_id_ctr, requirements[i][j], awards[i][j])
            execute(sql)

        closeConn(conn, cursor)

    # setup toolbar
    sys.stdout.write("Progress:")
    sys.stdout.write("  0.00%")
    sys.stdout.flush()
    sys.stdout.write("\b" * (6)) # return to start of line

    # Offices
    for i in range(nOffices):

        # TESTING
        # if i == 1:
        #     break

        conn, cursor, execute = openConn()

        auxPersons.clear()
        auxLeaders.clear()
        auxViceLeaders.clear()
        # gen leaders
        sql, person_id_ctr = pg.generate(cursor, 2, person_id_ctr, leaderMinBirthday, leaderMaxBirthday, auxPersons)
        execute(sql)
        sql, leader_id_ctr, leader_history_id_ctr = pg.leadergen(cursor, 2, leader_id_ctr, leader_history_id_ctr, auxPersons, False, auxLeaders, startDate)
        execute(sql)
        for p in auxPersons:
            award(cursor, p, 1, p)
            if p % 2 == 0:
                sql, leader_history_id_ctr = pg.leaderPause(cursor, leader_history_id_ctr, p, startDate, today, False)
                execute(sql)
        auxViceLeaders.append(auxLeaders[1])
        # gen office
        sql, office_id_ctr = eg.office.generate(cursor, 1, office_id_ctr, auxLeaders, auxViceLeaders, offices)
        execute(sql)

        # Outposts
        for j in range(nOutposts):

            # TESTING
            # if j == 1:
            #     break

            # update the bar
            s = "{percentage:.2f}".format(percentage = i * 2.5 + j * 0.05)
            if i * 2.5 + j * 0.05 < 10:
                s = " " + s
            sys.stdout.write("{}%".format(s))
            sys.stdout.flush()
            sys.stdout.write("\b" * (6)) # return to start of line

            auxPersons.clear()
            auxLeaders.clear()
            auxViceLeaders.clear()
            # gen leaders
            sql, person_id_ctr = pg.generate(cursor, 2, person_id_ctr, leaderMinBirthday, leaderMaxBirthday, auxPersons)
            execute(sql)
            sql, leader_id_ctr, leader_history_id_ctr = pg.leadergen(cursor, 2, leader_id_ctr, leader_history_id_ctr, auxPersons, False, auxLeaders, startDate)
            execute(sql)
            for p in auxPersons:
                award(cursor, p, 1, p)
                if p % 2 == 0:
                    sql, leader_history_id_ctr = pg.leaderPause(cursor, leader_history_id_ctr, p, startDate, today, False)
                    execute(sql)
            auxViceLeaders.append(auxLeaders[1])
            # gen outpost
            sql, outpost_id_ctr = eg.outpost.generate(cursor, 1, outpost_id_ctr, offices[i], auxLeaders, auxViceLeaders, outposts)
            execute(sql)

            # Divisions
            for k in range(nDivisions):
                auxPersons.clear()
                auxLeaders.clear()
                auxViceLeaders.clear()
                # gen leaders
                sql, person_id_ctr = pg.generate(cursor, 2, person_id_ctr, leaderMinBirthday, leaderMaxBirthday, auxPersons)
                execute(sql)
                sql, leader_id_ctr, leader_history_id_ctr = pg.leadergen(cursor, 2, leader_id_ctr, leader_history_id_ctr, auxPersons, False, auxLeaders, startDate)
                execute(sql)
                for p in auxPersons:
                    award(cursor, p, 1, p)
                    if p % 2 == 0:
                        sql, leader_history_id_ctr = pg.leaderPause(cursor, leader_history_id_ctr, p, startDate, today, False)
                        execute(sql)
                auxViceLeaders.append(auxLeaders[1])
                # gen division
                sql, division_id_ctr = eg.division.generate(cursor, 1, division_id_ctr, categories[k], outposts[j], auxLeaders, auxViceLeaders, divisions)
                execute(sql)

                # Teams
                for l in range(nTeams):
                    auxPersons.clear()
                    auxLeaders.clear()
                    auxTeams.clear()
                    auxViceLeaders.clear()
                    # gen leaders
                    sql, person_id_ctr = pg.generate(cursor, 2, person_id_ctr, leaderMinBirthday, leaderMaxBirthday, auxPersons)
                    execute(sql)
                    sql, leader_id_ctr, leader_history_id_ctr = pg.leadergen(cursor, 2, leader_id_ctr, leader_history_id_ctr, auxPersons, False, auxLeaders, startDate)
                    execute(sql)
                    for p in auxPersons:
                        award(cursor, p, 1, p)
                        if p % 2 == 0:
                            sql, leader_history_id_ctr = pg.leaderPause(cursor, leader_history_id_ctr, p, startDate, today, False)
                            execute(sql)
                    auxViceLeaders.append(auxLeaders[1])
                    # gen team
                    if l % 2 == 0:
                        gender = 'M'
                    else:
                        gender = 'F'
                    sql, team_id_ctr, leader_team_history_id_ctr = tg.generate(cursor, 1, team_id_ctr, leader_team_history_id_ctr, divisions[k], auxLeaders, auxViceLeaders, auxTeams, gender, startDate)
                    execute(sql)
                    sql, team_id_ctr, leader_team_history_id_ctr = tg.generate(cursor, 1, team_id_ctr, leader_team_history_id_ctr, divisions[k], auxLeaders, auxViceLeaders, auxTeams, gender, startDate)
                    execute(sql)

                    # Scouts
                    auxPersons.clear()
                    # gen scouts
                    sql, person_id_ctr = pg.generate(cursor, nScouts, person_id_ctr, scoutMinBirthdays[k], scoutMaxBirthdays[k], auxPersons, gender)
                    execute(sql)
                    sql, scout_id_ctr, scout_history_id_ctr, scout_team_history_id_ctr = pg.scoutgen(cursor, nScouts, scout_id_ctr, scout_history_id_ctr, scout_team_history_id_ctr, auxPersons, auxScouts, startDate, auxTeams[0], startDate)
                    execute(sql)
                    for p in auxPersons:
                        award(cursor, p, auxLeaders[0], p, categories[k])
                    for n in range(4):
                        sql, scout_history_id_ctr, scout_team_history_id_ctr = pg.scoutPause(cursor, scout_history_id_ctr, scout_team_history_id_ctr, auxPersons[n], startDate, today, auxTeams[1])
                        execute(sql)

        # Generate superfluous leaders for this office
        auxPersons.clear()
        auxLeaders.clear()
        for s in range(4098):
            sql, person_id_ctr = pg.generate(cursor, 1, person_id_ctr, leaderMinBirthday, leaderMaxBirthday, auxPersons)
            execute(sql)
            sql, leader_id_ctr, leader_history_id_ctr = pg.leadergen(cursor, 1, leader_id_ctr, leader_history_id_ctr, auxPersons, True, auxLeaders, startDate)
            execute(sql)
            award(cursor, auxPersons[s], 1, s)
            if s < 2500:
                sql, leader_team_history_id_ctr = tg.update(cursor, auxTeams[1], leader_team_history_id_ctr, junior_leader_id=auxLeaders[s], _date=today)
                execute(sql)
                sql, leader_history_id_ctr = pg.leaderPause(cursor, leader_history_id_ctr, auxPersons[s], startDate, today, False)
                execute(sql)
                sql, leader_team_history_id_ctr = tg.update(cursor, auxTeams[0], leader_team_history_id_ctr, leader_id=auxLeaders[s], _date=today)
                execute(sql)
            elif s < 3484:
                sql, leader_history_id_ctr = pg.leaderPause(cursor, leader_history_id_ctr, auxPersons[s], startDate, today, False)
                execute(sql)
                sql, leader_team_history_id_ctr = tg.update(cursor, auxTeams[0], leader_team_history_id_ctr, leader_id=auxLeaders[s], _date=today)
                execute(sql)
            elif s < 4000:
                sql, leader_team_history_id_ctr = tg.update(cursor, auxTeams[0], leader_team_history_id_ctr, leader_id=auxLeaders[s], _date=today)
                execute(sql)
        # commit for this office
        closeConn(conn, cursor)

    sys.stdout.write("\b done!  \n") # this ends the progress bar

    

def main():
    # Open connection
    conn, cursor, execute = openConn()

    # clear existing data
    print("Clearing data...")
    execute("SELECT * FROM clearall();")
    print("Generating data...")

    # division_category has only 3 rows
    division_category_id_ctr = 1
    sql, division_category_id_ctr = eg.division.categorygen(cursor, 3, division_category_id_ctr, ["Discovery", "Adventure", "Expedition"], categories)
    execute(sql)

    closeConn(conn, cursor)

    # Main generation
    start_time = time.time()
    generate()
    print("\nRuntime: %s seconds" % (time.time() - start_time))

main()