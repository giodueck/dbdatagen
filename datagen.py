'''Data generator for a postgresql project for uni'''

import psycopg2
# https://www.psycopg.org/docs/usage.html

# Connect to an existing database
conn = psycopg2.connect("dbname=datagentest user=postgres password=142857")

# Open a cursor to perform db operations
cursor = conn.cursor()


# Commit
conn.commit()

# Close communication with the db
cursor.close()
conn.close()