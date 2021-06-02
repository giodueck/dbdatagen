import miscgen
from os import name
import namegenerator

# Una idea posible para diferenciar awards de diferentes divisiones o para lideres es agregar una columna a award
def generate(cursor, c: int, ids: list, division_category_id: int = None, parent_award_id: int = None) -> str:
    '''Generate the SQL command to insert c new awards. They will be linearly dependent,
       i.e. the first award will be the parent to the second, the second to the third, etc.
        division_category_id: None if for leaders, otherwise give the appropriate id
        parent_award: award_id of the award to be the parent of the first generated award.'''
    # gen = DocumentGenerator()

    retstr = "INSERT INTO award (award_id, name, division_category_id, parent_award_id) VALUES "

    if division_category_id is None:
        division_category_id = 'null'

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "

        # award_id
        cursor.execute("SELECT * FROM nextval('award_award_id_seq');")
        seq = cursor.fetchone()
        id = seq[0]
        ids.append(id)
        
        # name
        # an = gen.word()
        an = namegenerator.gen(separator=' ')

        # parent_award_id for first loop
        if parent_award_id is None:
            parent_award_id = 'null'
        
        # add to SQL string
        retstr += "(" + str(id) + ",'" + an + "'," + str(division_category_id) + ',' + str(parent_award_id) + ")"

        # parent_award_id for other loops
        parent_award_id = id

    retstr += ';'

    return retstr

def requirementgen(cursor, c: int, ids: list, award_id: int) -> str:
    '''Generate the SQL command to insert c new requirements for the award award_id.'''

    retstr = "INSERT INTO requirement (requirement_id, award_id, description) VALUES "

    for i in range(c):
        # formatting
        if i > 0:
            retstr += ", "

        # requirement_id
        cursor.execute("SELECT * FROM nextval('requirement_requirement_id_seq');")
        seq = cursor.fetchone()
        id = seq[0]
        ids.append(id)
        
        # descrption
        des = miscgen.gensentence()
        
        # add to SQL string
        retstr += "(" + str(id) + ',' + str(award_id) + ",'" + des + "')"

    retstr += ';'

    return retstr