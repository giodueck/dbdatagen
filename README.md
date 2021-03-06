# dbdatagen - Generador de datos para la base de datos de Scouts con Python
Giovanni Dueck \
Adrian Ramirez 

# Cambios al diseño
!NO! Compatible con el diseño del Challenge 5 \
Usar el .architect en el repositorio
- award: columna division_category relaciona a cada award con una categoria de scouts. Para los awards de lideres se deja en null.
- leader_team_history: PK no estaba relacionada con una secuencia, se arregla en la version mas nueva.

Un backup se encuentra en el archivo dgtempty. Para restaurar el backup seleccionar formato Tar. \
La funcion clearall() elimina todos los datos y reestablece las secuencias para facilitar pruebas.

# Funcionamiento
Para ejecutar el programa ejecutar el script datagen.py \
Se crean de forma iterativa cada entidad con sus componentes, primero una office, luego sus outposts, luego las divisionees de cada outpost y los teams de cada division. Para cada entidad se generan los leaders justo antes. Los scouts se generan para cada team una vez exista. Para terminar la generacion de cada office se generan leaders superfluos para llegar a los 500K registros.\
Cada persona se genera con uno o varios awards, y la mayoria de los leaders y scouts salen y reentran en el programa.

ATENCION: El script elimina todos los datos existentes antes de cargar datos nuevos, puede tomar bastante tiempo.

persongen: generate crea una persona, leadergen y scoutgen generan filas a partir de una lista de person_ids. Para obtener un person/scout/leader_id valido se consulta e incrementa la secuencia asociada. Ademas agrega un registro a la tabla historica correspondiente; para agregar end_date o agregar un registro nuevo se tienen las funciones leaderLeave/scoutLeave y leaderRejoin/scoutRejoin

teamgen: funciones para crear y modificar un team.

entitygen: cada clase crea filas en la tabla de su nombre, division adicionalmente crea filas en division_category. Funciona de forma similar a persongen.

awardgen: generate crea awards con nombres aleatorios, y requirementgen genera requirements para un award usando un generador de oraciones. giveRequirement y genAward generan filas en person_requirement y person_award.

# Dependencies
command: "pip install pkgname"\
Paquetes:
- psycopg2: interface for postgresql
- names: name generator for persongen
- namegenerator: name generator for team name and requirement description
