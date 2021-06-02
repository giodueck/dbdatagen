import placenamegen as pngen
import names

class office:
    def generate(cursor, c: int, leader_ids: list, vice_leader_ids: list, ids: list, region: str = None) -> str:
        '''Generate the SQL command to insert a new office.'''

        retstr = "INSERT INTO office (office_id, leader_id, vice_leader_id, region) VALUES"

        for i in range(c):
            # formatting
            if i > 0:
                retstr += ", "

            # office_id
            cursor.execute("SELECT * FROM nextval('office_office_id_seq');")
            seq = cursor.fetchone()
            id = seq[0]
            ids.append(id)

            # region
            if region is None:
                region = pngen.generate()

            # add to SQL string
            retstr += "(" + str(id) + ',' + str(leader_ids[i]) + ',' + str(vice_leader_ids[i]) + ",'" + region + "')"
        
        retstr += ";"
        return retstr

class outpost:
    def generate(cursor, c: int, office_id: int, leader_ids: list, vice_leader_ids: list, ids: list, first_outpost_number: int = None) -> str:
        '''Generate the SQL command to insert a new outpost.'''

        retstr = "INSERT INTO outpost (outpost_id, office_id, leader_id, vice_leader_id, outpost_number, name) VALUES"

        for i in range(c):
            # formatting
            if i > 0:
                retstr += ", "

            # outpost_id and number
            cursor.execute("SELECT * FROM nextval('outpost_outpost_id_seq');")
            seq = cursor.fetchone()
            id = seq[0]
            ids.append(id)
            if i == 0 and first_outpost_number is None:
                first_outpost_number = id
            
            # name
            n = names.get_last_name()

            # add to SQL string
            retstr += "(" + str(id) + ',' + str(office_id) + ',' + str(leader_ids[i]) + ',' + str(vice_leader_ids[i]) + ',' + str(first_outpost_number + i) + ",'" + n + "')"
        
        retstr += ";"
        return retstr

class division:
    def categorygen(cursor, c: int, names: list, ids: list) -> str:
        '''Generate the SQL command to insert a new division category.'''
        
        retstr = "INSERT INTO division_category (division_category_id, name) VALUES "

        for i in range(c):
            # formatting
            if i > 0:
                retstr += ", "

            # division_category_id
            cursor.execute("SELECT * FROM nextval('division_category_division_category_id_seq_1');")
            seq = cursor.fetchone()
            id = seq[0]
            ids.append(id)

            # add to SQL string
            retstr += "(" + str(id) + ",'" + names[i] + "')"
        
        retstr += ";"
        return retstr
    
    def generate(cursor, c: int, division_category_id: int, outpost_ids: list, leader_ids: list, vice_leader_ids: list, ids: list) -> str:
        '''Generate the SQL command to insert a new division.'''

        retstr = "INSERT INTO division (division_id, division_category_id, outpost_id, leader_id, vice_leader_id) VALUES "

        for i in range(c):
            # formatting
            if i > 0:
                retstr += ", "

            # division_id
            cursor.execute("SELECT * FROM nextval('division_division_id_seq');")
            seq = cursor.fetchone()
            id = seq[0]
            ids.append(id)

            # add to SQL string
            retstr += '(' + str(id) + ',' + str(division_category_id) + ',' + str(outpost_ids[i]) + ',' + str(leader_ids[i]) + ',' + str(vice_leader_ids[i]) + ")"
        
        retstr += ";"
        return retstr