# dbdatagen - Generador de datos para la base de datos de Scouts con Python
Giovanni Dueck \
Adrian Ramirez 

Compatible con el diseño del Challenge 5

# Funcionamiento
persongen: generate crea una persona, leadergen y scoutgen generan filas a partir de una lista de person_ids. Para obtener un person/scout/leader_id valido se consulta e incrementa la secuencia asociada.
entitygen: cada clase crea filas en la tabla de su nombre, division adicionalmente crea filas en division_category. Funciona de forma similar a persongen

# Dependencies
command: "pip install pkgname"
- psycopg2
- names
