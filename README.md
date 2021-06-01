# dbdatagen - Generador de datos para la base de datos de Scouts con Python
Giovanni Dueck \
Adrian Ramirez 

Compatible con el diseño del Challenge 5

# Funcionamiento
Para ejecutar el programa ejecutar el script datagen.py

persongen: generate crea una persona, leadergen y scoutgen generan filas a partir de una lista de person_ids. Para obtener un person/scout/leader_id valido se consulta e incrementa la secuencia asociada.

teamgen: funciones para crear y modificar un team.

entitygen: cada clase crea filas en la tabla de su nombre, division adicionalmente crea filas en division_category. Funciona de forma similar a persongen.

Con respecto a tablas historicas: las tablas cuyos nombres terminan en _history deben ser actualizadas a la par que se generan datos en otras funciones, eso esta considerado para el futuro 

# Dependencies
command: "pip install pkgname"
- psycopg2: interface for postgresql
- names: name generator for persongen
- namegenerator: name generator for team name