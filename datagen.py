'''Data generator for a postgresql project for uni'''

import psycopg2
# https://www.psycopg.org/docs/usage.html
import persongen as pg
import entitygen as eg
import awardgen as ag
import teamgen as tg

from datetime import date
import sys

def openConn():
    '''Opens a connection to the db. Returns (conn, cursor) tuple.'''

    # Connect to an existing database
    conn = psycopg2.connect(database="datagentest", user="postgres", password=" ")

    # Open a cursor to perform db operations
    return conn, conn.cursor()

def closeConn(conn, cursor):
    '''Commits and closes connection to the db.'''

    # Commit
    conn.commit()

    # Close communication with the db
    cursor.close()
    conn.close()

conn, cursor = openConn()

def award(cursor, person_id: int, leader_id: int, i: int, category: int = None):
    '''Gives the person 1 or 2 awards depending on i'''

    # define award-list
    if category is not None:
        auxAwards = awards[category]
        auxReqs = requirements[category]
    else:
        auxAwards = awards[3]
        auxReqs = requirements[3]

    if i % 2 == 0:
        auxAwards = [auxAwards[0], auxAwards[1]]
        cursor.execute(ag.giveRequirements(person_id, auxReqs[0], leader_id, startDate, today))
        cursor.execute(ag.giveRequirements(person_id, auxReqs[1], leader_id, startDate, today))
    else:
        auxAwards = [auxAwards[0]]
        cursor.execute(ag.giveRequirements(person_id, auxReqs[0], leader_id, startDate, today))


    cursor.execute(ag.giveAwards(person_id, auxAwards, leader_id, startDate, today))

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

# clear existing data
print("Clearing data...")
cursor.execute("SELECT * FROM clearall();")
print("Generating data...")

# setup toolbar
sys.stdout.write("Progress:")
sys.stdout.write("  0.00%")
sys.stdout.flush()
sys.stdout.write("\b" * (6)) # return to start of line

# division_category has only 3 rows
cursor.execute(eg.division.categorygen(cursor, 3, ["Discovery", "Adventure", "Expedition"], categories))

closeConn(conn, cursor)

# Awards & requirements
for i in range(4):
    conn, cursor = openConn()

    # Awards
    awards.append(list())
    try:
        cursor.execute(ag.generate(cursor, nAwards, awards[i], categories[i]))
    except:
        # leader awards will cause an exception because of categories
        cursor.execute(ag.generate(cursor, nAwards, awards[i], None))

    # Requirements
    requirements.append(list())
    for j in range(len(awards[i])):
        requirements[i].append(list())
        cursor.execute(ag.requirementgen(cursor, nReqs, requirements[i][j], awards[i][j]))

    closeConn(conn, cursor)

# Offices
for i in range(nOffices):

    # TESTING
    # if i == 1:
    #     break

    conn, cursor = openConn()

    auxPersons.clear()
    auxLeaders.clear()
    auxViceLeaders.clear()
    # gen leaders
    cursor.execute(pg.generate(cursor, 2, leaderMinBirthday, leaderMaxBirthday, auxPersons))
    cursor.execute(pg.leadergen(cursor, 2, auxPersons, False, auxLeaders, startDate))
    for p in auxPersons:
        award(cursor, p, 1, p)
        if p % 2 == 0:
            cursor.execute(pg.leaderPause(cursor, p, startDate, today, False))
    auxViceLeaders.append(auxLeaders[1])
    # gen office
    cursor.execute(eg.office.generate(cursor, 1, auxLeaders, auxViceLeaders, offices))

    # Outposts
    for j in range(nOutposts):

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
        cursor.execute(pg.generate(cursor, 2, leaderMinBirthday, leaderMaxBirthday, auxPersons))
        cursor.execute(pg.leadergen(cursor, 2, auxPersons, False, auxLeaders, startDate))
        for p in auxPersons:
            award(cursor, p, 1, p)
            if p % 2 == 0:
                cursor.execute(pg.leaderPause(cursor, p, startDate, today, False))
        auxViceLeaders.append(auxLeaders[1])
        # gen outpost
        cursor.execute(eg.outpost.generate(cursor, 1, offices[i], auxLeaders, auxViceLeaders, outposts))

        # Divisions
        for k in range(nDivisions):
            auxPersons.clear()
            auxLeaders.clear()
            auxViceLeaders.clear()
            # gen leaders
            cursor.execute(pg.generate(cursor, 2, leaderMinBirthday, leaderMaxBirthday, auxPersons))
            cursor.execute(pg.leadergen(cursor, 2, auxPersons, False, auxLeaders, startDate))
            for p in auxPersons:
                award(cursor, p, 1, p)
                if p % 2 == 0:
                    cursor.execute(pg.leaderPause(cursor, p, startDate, today, False))
            auxViceLeaders.append(auxLeaders[1])
            # gen division
            cursor.execute(eg.division.generate(cursor, 1, categories[k], outposts[j], auxLeaders, auxViceLeaders, divisions))

            # Teams
            for l in range(nTeams):
                auxPersons.clear()
                auxLeaders.clear()
                auxTeams.clear()
                auxViceLeaders.clear()
                # gen leaders
                cursor.execute(pg.generate(cursor, 2, leaderMinBirthday, leaderMaxBirthday, auxPersons))
                cursor.execute(pg.leadergen(cursor, 2, auxPersons, False, auxLeaders, startDate))
                for p in auxPersons:
                    award(cursor, p, 1, p)
                    if p % 2 == 0:
                        cursor.execute(pg.leaderPause(cursor, p, startDate, today, False))
                auxViceLeaders.append(auxLeaders[1])
                # gen team
                if l % 2 == 0:
                    gender = 'M'
                else:
                    gender = 'F'
                cursor.execute(tg.generate(cursor, 1, divisions[k], auxLeaders, auxViceLeaders, auxTeams, gender, startDate))
                cursor.execute(tg.generate(cursor, 1, divisions[k], auxLeaders, auxViceLeaders, auxTeams, gender, startDate))

                # Scouts
                auxPersons.clear()
                # gen scouts
                cursor.execute(pg.generate(cursor, nScouts, scoutMinBirthdays[k], scoutMaxBirthdays[k], auxPersons, gender))
                cursor.execute(pg.scoutgen(cursor, nScouts, auxPersons, auxScouts, startDate, auxTeams[0], startDate))
                for p in auxPersons:
                    award(cursor, p, auxLeaders[0], p, categories[k])
                for n in range(4):
                    cursor.execute(pg.scoutPause(cursor, auxPersons[n], startDate, today, auxTeams[1]))

    # Generate superfluous leaders for this office
    auxPersons.clear()
    auxLeaders.clear()
    for s in range(4098):
        cursor.execute(pg.generate(cursor, 1, leaderMinBirthday, leaderMaxBirthday, auxPersons))
        cursor.execute(pg.leadergen(cursor, 1, auxPersons, True, auxLeaders, startDate))
        award(cursor, auxPersons[s], 1, s)
        if s < 3484:
            cursor.execute(pg.leaderPause(cursor, auxPersons[s], startDate, today, False))
        if s < 4000:
            cursor.execute(tg.update(cursor, auxTeams[0], leader_id=auxLeaders[s], _date=today))
        if s < 2500:
            cursor.execute(tg.update(cursor, auxTeams[1], junior_leader_id=auxLeaders[s], _date=today))

    # commit for this office
    closeConn(conn, cursor)

sys.stdout.write("\b done!  \n") # this ends the progress bar