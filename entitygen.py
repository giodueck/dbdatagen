import placenamegen as pngen
import names

class office:
    def generate(cursor, c: int, id_ctr: int, leader_ids: list, vice_leader_ids: list, ids: list, region: str = None) -> str:
        '''Generate the SQL command to insert a new office.'''

        execute = cursor.execute
        fetchone = cursor.fetchone

        retstr = "INSERT INTO office (office_id, leader_id, vice_leader_id, region) VALUES"

        for i in range(c):
            # formatting
            if i > 0:
                retstr = "".join([retstr, ", "])

            # office_id
            # execute("SELECT * FROM nextval('office_office_id_seq');")
            # seq = fetchone()
            # id = seq[0]
            ids.append(id_ctr)

            # region
            if region is None:
                region = pngen.generate()

            # add to SQL string
            sql = "(%s,%s,%s,'%s')" % (str(id_ctr), str(leader_ids[i]), str(vice_leader_ids[i]), region)
            retstr = "".join([retstr, sql])

            id_ctr += 1
        
        retstr = "".join([retstr, ";"])
        return retstr, id_ctr

class outpost:
    def generate(cursor, c: int, id_ctr: int, office_id: int, leader_ids: list, vice_leader_ids: list, ids: list, first_outpost_number: int = None) -> str:
        '''Generate the SQL command to insert a new outpost.'''

        execute = cursor.execute
        fetchone = cursor.fetchone

        retstr = "INSERT INTO outpost (outpost_id, office_id, leader_id, vice_leader_id, outpost_number, name) VALUES"

        for i in range(c):
            # formatting
            if i > 0:
                retstr = "".join([retstr, ", "])

            # outpost_id and number
            # execute("SELECT * FROM nextval('outpost_outpost_id_seq');")
            # seq = fetchone()
            # id = seq[0]
            ids.append(id_ctr)
            if i == 0 and first_outpost_number is None:
                first_outpost_number = id_ctr
            
            # name
            n = names.get_last_name()

            # add to SQL string
            sql = "(%s,%s,%s,%s,%s,'%s')" % (str(id_ctr), str(office_id), str(leader_ids[i]), str(vice_leader_ids[i]), str(first_outpost_number + i), n)
            retstr = "".join([retstr, sql])

            id_ctr += 1

        retstr = "".join([retstr, ";"])
        return retstr, id_ctr

class division:
    def categorygen(cursor, c: int, id_ctr: int, names: list, ids: list) -> str:
        '''Generate the SQL command to insert a new division category.'''
        
        execute = cursor.execute
        fetchone = cursor.fetchone

        retstr = "INSERT INTO division_category (division_category_id, name) VALUES "

        for i in range(c):
            # formatting
            if i > 0:
                retstr = "".join([retstr, ", "])

            # division_category_id
            # execute("SELECT * FROM nextval('division_category_division_category_id_seq_1');")
            # seq = fetchone()
            # id = seq[0]
            ids.append(id_ctr)

            # add to SQL string
            sql = "(%s,'%s')" % (str(id_ctr), names[i])
            retstr = "".join([retstr, sql])

            id_ctr += 1
        
        retstr = "".join([retstr, ";"])
        return retstr, id_ctr
    
    def generate(cursor, c: int, id_ctr: int, division_category_id: int, outpost_id: int, leader_ids: list, vice_leader_ids: list, ids: list) -> str:
        '''Generate the SQL command to insert a new division.'''

        execute = cursor.execute
        fetchone = cursor.fetchone

        retstr = "INSERT INTO division (division_id, division_category_id, outpost_id, leader_id, vice_leader_id) VALUES "

        for i in range(c):
            # formatting
            if i > 0:
                retstr = "".join([retstr, ", "])

            # division_id
            # execute("SELECT * FROM nextval('division_division_id_seq');")
            # seq = fetchone()
            # id = seq[0]
            ids.append(id_ctr)

            # add to SQL string
            sql = "(%s,%s,%s,%s,%s)" % (str(id_ctr), str(division_category_id), str(outpost_id), str(leader_ids[i]), str(vice_leader_ids[i]))
            retstr = "".join([retstr, sql])

            id_ctr += 1

        retstr = "".join([retstr, ";"])
        return retstr, id_ctr