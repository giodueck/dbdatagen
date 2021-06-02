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
pids = list()
lids = list()
sids = list()
tids = list()

oids = list()
opids = list()
dcids = list()
dids = list()

aids = list()
rids = list()

print("Generating rows for...")

# leaders
print("                   ...person->leader")
cursor.execute(pg.generate(cursor, 10, date(1990, 1, 1), date(2000, 12, 31), pids))
cursor.execute(pg.leadergen(cursor, 10, pids, False, lids))

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
pids.clear()
lids.clear()
cursor.execute(pg.generate(cursor, 1, date(1990, 1, 1), date(2000, 12, 31), pids, 'M'))
cursor.execute(pg.generate(cursor, 1, date(1990, 1, 1), date(2000, 12, 31), pids, 'F'))
cursor.execute(pg.leadergen(cursor, 2, pids, False, lids))

    # teams
print("                   ...team")
cursor.execute(tg.generate(cursor, 1, dids[0], lids, tids, 'M', date(2021, 6, 1)))
lids.pop(0)
cursor.execute(tg.generate(cursor, 1, dids[0], lids, tids, 'F', date(2021, 6, 1)))
lids.pop(0)

# scouts
print("                   ...person->scout")
pids.clear()
cursor.execute(pg.generate(cursor, 10, date(2005, 1, 1), date(2008, 12, 31), pids, 'M'))
cursor.execute(pg.scoutgen(cursor, 10, pids, sids, tids[0]))
pids.clear()
cursor.execute(pg.generate(cursor, 10, date(2005, 1, 1), date(2008, 12, 31), pids, 'F'))
cursor.execute(pg.scoutgen(cursor, 10, pids, sids, tids[1]))

# awards
print("                   ...award")
cursor.execute(ag.generate(cursor, 3, aids, dcids[0]))

# requirements
print("                   ...requirement")
for i in range(len(aids)):
    rids.append(list())
    cursor.execute(ag.requirementgen(cursor, 3, rids[i], aids[i]))

# Commit
conn.commit()

# Close communication with the db
cursor.close()
conn.close()