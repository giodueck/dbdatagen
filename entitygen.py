import placenamegen as pngen

class office:
    def generate(leader_id: int, vice_leader_id: int, region: str = None) -> str:
        '''Generate the SQL command to insert a new office.'''

        retstr = "INSERT INTO office (leader_id, vice_leader_id, region) VALUES ("

        if region is None:
            region = pngen.generate()
        
        return retstr + str(leader_id) + ',' + str(vice_leader_id) + ',' + region + ");"

class outpost:
    def generate(office_id: int, leader_id: int, vice_leader_id: int, outpost_number: int) -> str:
        '''Generate the SQL command to insert a new outpost.'''

        retstr = "INSERT INTO outpost (office_id, leader_id, vice_leader_id, outpost_number) VALUES "

        return retstr + '(' + str(office_id) + ',' + str(leader_id) + ',' + str(vice_leader_id) + ',' + str(outpost_number) + ");"

class division:
    def categorygen(name: str) -> str:
        '''Generate the SQL command to insert a new division category.'''
        
        retstr = "INSERT INTO division_category (name) VALUES "

        return retstr + '(' + name + ");"
    
    def generate(division_category_id: int, outpost_id: int, leader_id: int, vice_leader_id: int) -> str:
        '''Generate the SQL command to insert a new division.'''

        retstr = "INSERT INTO division (division_category_id, outpost_id, leader_id, vice_leader_id) VALUES "

        return retstr + '(' + str(division_category_id) + ',' + str(outpost_id) + ',' + str(leader_id) + ',' + str(vice_leader_id) + ");"