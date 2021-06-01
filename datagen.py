'''Data generator for a postgresql project for uni'''

import psycopg2
# https://www.psycopg.org/docs/usage.html

# Connect to an existing database
conn = psycopg2.connect(database="datagentest", user="postgres", password=" ")

# Open a cursor to perform db operations
cursor = conn.cursor()

# Cuando tenga hechas todas las funciones para cada tabla el script en si va a estar aqui


# Commit
conn.commit()

# Close communication with the db
cursor.close()
conn.close()