'''Data generator for a postgresql project for uni'''

import psycopg2
# https://www.psycopg.org/docs/usage.html
import persongen as pg
import entitygen as eg
from datetime import date
import teamgen as tg
import awardgen as ag

# Connect to an existing database
conn = psycopg2.connect(database="datagentest", user="postgres", password=" ")

# Open a cursor to perform db operations
cursor = conn.cursor()

# Lists to store created ids
lpids = list()
tlpids = list()
spids1 = list()
spids2 = list()

lids = list()
lhids = list()
tlids = list()
tlhids = list()

sids = list()
sthids = list()
shids = list()
tids = list()
lthids = list()

oids = list()
opids = list()
dcids = list()
dids = list()

aids = list()
rids = list()

# clear existing data
print("Clearing data...")
cursor.execute("SELECT * FROM clearall();")

print("Generating rows for...")

# leaders
print("                   ...person->leader")
cursor.execute(pg.generate(cursor, 10, date(1990, 1, 1), date(2000, 12, 31), lpids))
cursor.execute(pg.leadergen(cursor, 10, lpids, False, lids, lhids, date(2021, 3, 14)))

# offices
print("                   ...office")
ol = list(); ol.append(lids.pop(0))
ovl = list(); ovl.append(lids.pop(0))
cursor.execute(eg.office.generate(cursor, 1, ol, ovl, oids))

# ouposts
print("                   ...outpost")
opl = list(); opl.append(lids.pop(0)); opl.append(lids.pop(0))
opvl = list(); opvl.append(lids.pop(0)); opvl.append(lids.pop(0))
cursor.execute(eg.outpost.generate(cursor, 2, oids[0], opl, opvl, opids))

# divisions
print("                   ...division_category")
cursor.execute(eg.division.categorygen(cursor, 1, ["Default"], dcids))

print("                   ...division")
dl = list(); dl.append(lids.pop(0)); dl.append(lids.pop(0))
dvl = list(); dvl.append(lids.pop(0)); dvl.append(lids.pop(0))
cursor.execute(eg.division.generate(cursor, 2, dcids[0], opids, dl, dvl, dids))

# teams
    # leaders
print("                   ...person->leader->team")
cursor.execute(pg.generate(cursor, 1, date(1990, 1, 1), date(2000, 12, 31), tlpids, 'M'))
cursor.execute(pg.generate(cursor, 1, date(1990, 1, 1), date(2000, 12, 31), tlpids, 'F'))
cursor.execute(pg.leadergen(cursor, 2, tlpids, False, tlids, tlhids, date(2021, 3, 14)))

    # teams
print("                   ...team")
cursor.execute(tg.generate(cursor, 1, dids[0], tlids, tids, 'M', date(2021, 6, 1), lthids))
auxtlids = [tlids[1]]
cursor.execute(tg.generate(cursor, 1, dids[0], auxtlids, tids, 'F', date(2021, 6, 1), lthids))

# scouts
print("                   ...person->scout")
cursor.execute(pg.generate(cursor, 10, date(2005, 1, 1), date(2008, 12, 31), spids1, 'M'))
cursor.execute(pg.scoutgen(cursor, 10, spids1, sids, shids, date(2021, 3, 18), tids[0], date(2021, 3, 18), sthids))
cursor.execute(pg.generate(cursor, 10, date(2005, 1, 1), date(2008, 12, 31), spids2, 'F'))
cursor.execute(pg.scoutgen(cursor, 10, spids2, sids, shids, date(2021, 3, 18), tids[1], date(2021, 3, 18), sthids))

# awards
print("                   ...award")
cursor.execute(ag.generate(cursor, 3, aids, dcids[0]))

# requirements
print("                   ...requirement")
for i in range(len(aids)):
    rids.append(list())
    cursor.execute(ag.requirementgen(cursor, 3, rids[i], aids[i]))

# assign met requirements
print("                   ...person_requirement")
for i in range(len(spids1)):
    for j in range(len(aids)):
        redrids = [rids[j][0]]
        if i % 2 == 0:
            redrids.append(rids[j][1])
            if i % 4 == 0:
                redrids.append(rids[j][2])

        cursor.execute(ag.giveRequirements(spids1[i], redrids, tlids[0], date(2020,1,1), date(2020,12,31)))
        cursor.execute(ag.giveRequirements(spids2[i], redrids, tlids[1], date(2020,1,1), date(2020,12,31)))

# assign awards
print("                   ...person_award")
for i in range(len(spids1)):
    redaids = [aids[0]]
    if i % 2 == 0:
        redaids.append(aids[1])
        if i % 4 == 0:
            redaids.append(aids[2])
    cursor.execute(ag.giveAwards(spids1[i], redaids, tlids[0], date(2020,1,1), date(2020,12,31)))
    cursor.execute(ag.giveAwards(spids2[i], redaids, tlids[1], date(2020,1,1), date(2020,12,31)))

# leavers
leaverlpids = list()
leaverlids = list()
leaverlhids = list()
leaverspids = list()
leaversids = list()
leavershids = list()
print("                   ...person->leader->leave")
cursor.execute(pg.generate(cursor, 2, date(1990, 1, 1), date(2000, 12, 31), leaverlpids, 'M'))
cursor.execute(pg.leadergen(cursor, 2, leaverlpids, True, leaverlids, leaverlhids, date(2021, 3, 14)))
for id in leaverlpids:
    cursor.execute(pg.leaderLeave(id, date(2021, 4, 15)))
cursor.execute(pg.leaderRejoin(cursor, leaverlpids[0], False, leaverlhids, date(2021, 5, 15)))
print("                   ...person->scout->leave")
cursor.execute(pg.generate(cursor, 2, date(2005, 1, 1), date(2008, 12, 31), leaverspids, 'F'))
cursor.execute(pg.scoutgen(cursor, 2, leaverspids, leaversids, leavershids, date(2021, 3, 18), tids[1], date(2021, 3, 18), sthids))
for id in leaverspids:
    cursor.execute(pg.scoutLeave(cursor, id, date(2021, 4, 15)))
cursor.execute(pg.scoutRejoin(cursor, leaverspids[0], leavershids, date(2021, 5, 15), tids[1], date(2021, 5, 15), sthids))

# switch team leader for team 1
print("                   ...replace team leader")
cursor.execute(tg.replaceTeamLeader(cursor, tids[0], leaverlids[0], False, date(2021, 4, 15), lthids))

# add junior leader to team 1
print("                   ...add junior team leader")
cursor.execute(tg.replaceTeamLeader(cursor, tids[0], tlids[0], True, date(2021, 4, 15), lthids))

# Commit
conn.commit()

# Close communication with the db
cursor.close()
conn.close()