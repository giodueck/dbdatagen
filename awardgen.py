import miscgen
import namegenerator
from datetime import date

# Una idea posible para diferenciar awards de diferentes divisiones o para lideres es agregar una columna a award
def generate(cursor, c: int, id_ctr: int, ids: list, division_category_id: int = None, parent_award_id: int = None) -> str:
    '''Generate the SQL command to insert c new awards. They will be linearly dependent,
       i.e. the first award will be the parent to the second, the second to the third, etc.
        division_category_id: None if for leaders, otherwise give the appropriate id
        parent_award: award_id of the award to be the parent of the first generated award.'''
    # gen = DocumentGenerator()

    execute = cursor.execute
    # fetchone = cursor.fetchone

    retstr = "INSERT INTO award (award_id, name, division_category_id, parent_award_id) VALUES "

    if division_category_id is None:
        division_category_id = 'null'

    for i in range(c):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])

        # award_id
        # execute("SELECT * FROM nextval('award_award_id_seq');")
        # seq = fetchone()
        # id = seq[0]
        ids.append(id_ctr)
        
        # name
        an = namegenerator.gen(separator=' ')

        # parent_award_id for first loop
        if parent_award_id is None:
            parent_award_id = 'null'
        
        # add to SQL string
        sql = "(%s,'%s',%s,%s)" % (str(id_ctr), an, str(division_category_id), str(parent_award_id))
        retstr = "".join([retstr, sql])

        # parent_award_id for other loops
        parent_award_id = id_ctr
        id_ctr += 1

    retstr = "".join([retstr, ";"])

    return retstr, id_ctr

def requirementgen(cursor, c: int, id_ctr: int, ids: list, award_id: int) -> str:
    '''Generate the SQL command to insert c new requirements for the award award_id.'''

    execute = cursor.execute
    fetchone = cursor.fetchone

    retstr = "INSERT INTO requirement (requirement_id, award_id, description) VALUES "

    for i in range(c):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])

        # requirement_id
        # execute("SELECT * FROM nextval('requirement_requirement_id_seq');")
        # seq = fetchone()
        # id = seq[0]
        ids.append(id_ctr)
        
        # descrption
        des = namegenerator.gen()   # generar una frase usando cadenas de Markov tomaba tiempo inecesariamente
        
        # add to SQL string
        sql = "(%s,%s,'%s')" % (str(id_ctr), str(award_id), des)
        retstr = "".join([retstr, sql])

        id_ctr += 1

    retstr = "".join([retstr, ';'])

    return retstr, id_ctr

def giveRequirements(person_id: int, rids: list, leader_id: int, minDate: date, maxDate: date):
    '''Generate the SQL command to insert new rows into person_requirement.
        person_id: person to be given the requirements       
        rids: list of requirements
        leader_id: leader that certifies the requirement is met
        min/maxDate: range of generated dates
    '''

    retstr = "INSERT INTO person_requirement (person_id, requirement_id, \"date\", leader_id) VALUES "

    for i in range(len(rids)):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])
        
        # date
        rd = miscgen.gendate(minDate, maxDate)
        
        # add to SQL string
        sql = "(%s,%s,'%s',%s)" % (str(person_id), str(rids[i]), str(rd), str(leader_id))
        retstr = "".join([retstr, sql])

    retstr = "".join([retstr, ';'])

    return retstr

def giveAwards(person_id: int, aids: list, leader_id: int, minDate: date, maxDate: date):
    '''Generate the SQL command to insert new rows into person_award.
        person_id: person to be given the awards
        aids: list of awards
        leader_id: leader that certifies the award
        min/maxDate: range of generated dates
    '''

    retstr = "INSERT INTO person_award (person_id, award_id, \"date\", leader_id) VALUES "

    for i in range(len(aids)):
        # formatting
        if i > 0:
            retstr = "".join([retstr, ", "])
        
        # date
        rd = miscgen.gendate(minDate, maxDate)
        
        # add to SQL string
        sql = "(%s,%s,'%s',%s)" % (str(person_id), str(aids[i]), str(rd), str(leader_id))
        retstr = "".join([retstr, sql])

    retstr = "".join([retstr, ';'])

    return retstr