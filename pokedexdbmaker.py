import hidden
import requests
import psycopg2
from psycopg2 import sql

# hidden.py is a file that will hold your postgres database information
# You could hard code it.
secrets = hidden.secrets()

# createPokedex uses a txt file created by txtPokedex to write to a postgres
# database. Splitting the pokeAPI call from the "db migration" is sanity
# and error checking
def createPokedex(secrets, file_name):
    db_info = secrets
    conn = psycopg2.connect(database=db_info['database'],
                            user=db_info['user'],
                            host=db_info['host'],
                            password=db_info['pass'],
                            port=db_info['port'])
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS pokedex""")
    cur.execute("""CREATE TABLE pokedex(
                id INTEGER PRIMARY KEY,
                poke_name VARCHAR (50) UNIQUE NOT NULL,
                poke_type_1 VARCHAR (20) NOT NULL,
                poke_type_2 VARCHAR (20),
                evo_id INTEGER);
                """)
    conn.commit()
    print("Table created successfully")
    file = open(file_name, "r")
    file.readline()
    for line in file:
        line = line.strip()
        items = line.split()
        if (len(items) == 3):
            id = items[0]
            name = items[1]
            type_1 = items[2]
            cur.execute("""INSERT INTO pokedex(id, poke_name,
                        poke_type_1) VALUES (%s, %s, %s);""",
                        (id, name, type_1))
        else:
            id = items[0]
            name = items[1]
            type_1 = items[2]
            type_2 = items[3]
            cur.execute("""INSERT INTO pokedex(id, poke_name,
                        poke_type_1, poke_type_2) VALUES
                        (%s, %s, %s, %s);""",
                        (id, name, type_1, type_2))
        print(f"Inserted {name} into pokedex")
    file.close()
    conn.commit()
    conn.close()


def findEvolutionLines(secrets, min_id: int, max_id: int):
    db_info = secrets
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["pass"],
                            port=db_info['port'])
    cur = conn.cursor()
    base_url = "https://pokeapi.co/api/v2/evolution-chain/"
    for i in range(min_id, max_id):
        url = base_url + str(i)
        print(f"Getting data from: {url}")
        pokes = []
        response = requests.get(url)
        raw_data = response.json()
        chain = raw_data.get("chain")
        base_species = chain.get('species').get('name')
        pokes.append(base_species)
        evolves_to = chain.get("evolves_to")
        for evo in evolves_to:
            if len(evo.get("evolves_to")) > 0:
                third = evo.get("evolves_to")
                pokes.append(third[0].get("species").get("name"))
            second = evo.get("species").get("name")
            pokes.append(second)
        for poke in pokes:
            try:
                cur.execute(sql.SQL("""UPDATE pokedex SET evo_id = %s WHERE
                                    poke_name = %s"""), (i, poke,))
            except psycopg2.Error as err:
                print(err)
                print(f"Something went wrong with id = {i}")
                continue

    conn.commit()
    conn.close()


def txtPokedex(file_name: str, minId: None, maxId: None):
    min_id = 0
    max_id = 1025
    if (type(minId) is int) and (type(maxId) is int):
        if minId < maxId:
            min_id = minId
            max_id = maxId

    f = open(file_name, "w")
    f.write("id name type1 type2\n")
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    for i in range(min_id, max_id+1):
        url = base_url + str(i)
        response = requests.get(url)
        id = i
        name = response.json().get('name')
        types = response.json().get('types')
        row = str(id) + " " + name
        for t in types:
            type_n = t.get("type").get("name")
            row = row + " " + type_n
        f.write(row + "\n")
    f.close()


def pokedexHelper():
    file_name = input("Enter desired pokedex txt file name e.g 'redanbluedex.txt':")
    print("Next we will for the range of pokemon id's to be searched")
    print("You can check websites such as serebii.net or bulbapedia for correct")
    print("id ranges for a given game. Use national dex numbers.")
    min_id = input("Enter lowest pokemon id in the game:")
    max_id = input("Enter highest pokemon id in the game:")
    txtPokedex(file_name, int(min_id), int(max_id))
    createPokedex(secrets, file_name)
    findEvolutionLines(min_id, max_id)


#pokedexHelper()
#txtPokedex("reddex.txt", 1, 151)
#createPokedex(secrets, "reddex.txt")
findEvolutionLines(secrets, 1, 151)

