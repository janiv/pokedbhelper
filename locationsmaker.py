import hidden
import requests
import psycopg2
from psycopg2 import sql
from typing import List


def findLocations(gameName: str, id: int):
    file_name = gameName + "_locations.txt"
    f = open(file_name, "w")
    f.write("location_id, location_name, location_url\n")
    url = "https://pokeapi.co/api/v2/region/" + str(id)
    response = requests.get(url)
    print(response)
    locations = response.json().get('locations')
    for location in locations:
        resp2 = requests.get(location.get('url'))
        id = resp2.json().get('id')
        f.write(str(id) + ", " + location.get('name') + ", " +
                location.get('url') + '\n')
    f.close()
    return file_name


def findLocationAreasURL(gameName: str, location_file_name: str):
    # We need to write code such that for each location we go to all location
    # areas, and write them to a txt file.
    f = open(location_file_name, 'r')
    data = f.readlines()
    f.close()
    loc_area_file_name = gameName + "_location_areas.txt"
    loc_area_f = open(loc_area_file_name, "w")
    data = data[1:]
    for line in data:
        line = line.split(", ")
        name = line[1].strip()
        url = line[2].strip()
        print(url)
        response = requests.get(url)
        areas = response.json().get('areas')
        # May have many areas
        areas_string = name
        for area in areas:
            areas_string = areas_string + " " + area.get("url")
        loc_area_string = line[0].strip() + " " + areas_string + "\n"
        loc_area_f.write(loc_area_string)
    loc_area_f.close()
    return loc_area_file_name


def getID(db_key: dict, poke_name: str, gen_pokedex: str) -> str:
    db_info = db_key
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["password"],
                            port=db_info['port'])
    cur = conn.cursor()
    if poke_name == "basculin-blue-striped":
        poke_name = "basculin-red-striped"
    #query = "SELECT id FROM pokedex where poke_name = %s;"
    cur.execute(sql.SQL("""SELECT id FROM {} where poke_name = %s""")
             .format(sql.Identifier(f'{gen_pokedex}')), (poke_name,))
    result = cur.fetchone()
    return result


def createDB(location_area_name: str, pokes: List[str], methods: List[str],
             db_key: dict, gen_pokedex:str):
    db_info = db_key
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["password"],
                            port=db_info['port'])
    cur = conn.cursor()
    print("Attempting to create: " + location_area_name)
    area_name = location_area_name.strip()
    cur.execute(sql.SQL("""CREATE TABLE IF NOT EXISTS {} (
                    poke_id integer NOT NULL PRIMARY KEY,
                    pokemon VARCHAR (30) NOT NULL,
                    encounter_method VARCHAR(30) NOT NULL);""")
                .format(sql.Identifier(f'{area_name}')))
    for i in range(len(pokes)):
        print(pokes[i])
        id = getID(db_key, pokes[i], gen_pokedex)[0]
        poke = pokes[i]
        meth = methods[i]
        print("pokemon: " + poke)
        print("id: " + str(id))
        print("meth: " + meth)
        cur.execute(sql.SQL("""INSERT INTO {} (poke_id, pokemon,
                                encounter_method)
                            VALUES(%s,%s, %s) ON CONFLICT DO NOTHING""",)
                    .format(sql.Identifier(f'{area_name}')), (id, poke, meth,))

    conn.commit()
    conn.close()

def add_evo_lines(table_names:str, game_name:str, db_key: dict):
    db_info = db_key
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["password"],
                            port=db_info['port'])
    cur = conn.cursor()
    file = open(table_names, "r")
    routes = file.readlines()
    routes = routes[2:]
    for route in routes:
        route = route.strip()
        route = game_name + "_" + route
        cur.execute(sql.SQL("""ALTER TABLE {} ADD evo_line_id INTEGER;""").format(sql.Identifier(f'{route}')),)
    conn.commit()
    cur.close()
    conn.close()

def update_evo_lines(table_names:str, game_name:str, db_key: dict, pokedex_name:str):
    db_info = db_key
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["password"],
                            port=db_info['port'])
    cur = conn.cursor()
    file = open(table_names, "r")
    routes = file.readlines()
    file.close()
    routes = routes[2:]
    for route in routes:
        route = route.strip()
        route = game_name + "_" + route
        cur.execute(sql.SQL("""SELECT poke_id FROM {};""").format(sql.Identifier(f'{route}')),)
        ids = cur.fetchall()
        for id in ids:
            raw_id = id[0]
            cur.execute(sql.SQL("""SELECT evo_id FROM {} WHERE id=%s""").format(sql.Identifier(f'{pokedex_name}')), (raw_id,))
            evo_id_tuple = cur.fetchone()
            evo_id = evo_id_tuple[0]
            cur.execute(sql.SQL("""UPDATE {} SET evo_line_id = %s WHERE poke_id=%s""").format(sql.Identifier(f'{route}')), (evo_id, raw_id))
    conn.commit()
    cur.close()
    conn.close()


def createLocation_Area_Tables(location_areas_file: str, game_name: str,
                               db_key: dict, gen_pokedex:str):
    file = open(location_areas_file, 'r')
    for line in file:
        line = line.strip()
        data = line.split()
        table_name = data[1]
        data = data[2:]
        valid_pokes = []
        encounter_methods = []
        for url in data:
            url = url.strip()
            print(f"Trying to access: {url}")
            try:
                response = requests.get(url, timeout=10)
            except requests.exceptions.Timeout:
                print("Timed out")
                continue
            location_area_data = response.json()
            encounters = location_area_data.get("pokemon_encounters")
            for poke in encounters:
                pokemon = poke.get("pokemon")
                version_detail = poke.get("version_details")  # This is a list
                for game in version_detail:
                    version = game.get("version")
                    if (version.get("name") == game_name):
                        if (pokemon.get("name") not in valid_pokes):
                            valid_pokes.append(pokemon.get("name"))
                            enc_meth = game.get('encounter_details')[0].get('method').get('name')
                            encounter_methods.append(enc_meth)
        if (len(valid_pokes) == 0): continue
        table_name = table_name.replace("-", "_")
        table_name = game_name + "_" + table_name
        createDB(table_name, valid_pokes, encounter_methods,
                 db_key, gen_pokedex)

#createLocation_Area_Tables(location_areas_file="red_location_areas.txt",
#                           game_name="red", db_key=hidden.secrets(),
#                           gen_pokedex="gen_1_pokedex")
#games = [("red", "kanto_locations.txt"), ("blue", "kanto_locations.txt"), ("yellow", "kanto_locations.txt"),
#         ("silver", "johto_locations.txt"),("gold", "johto_locations.txt"),("crystal", "johto_locations.txt"),
#         ("ruby", "hoenn_locations.txt"), ("sapphire", "hoenn_locations.txt"), ("emerald", "hoenn_locations.txt"),
#         ("leafgreen", "kanto_locations.txt"), ("firered", "kanto_locations.txt"),
#         ("pearl", "sinnoh_locations.txt"),("diamond", "sinnoh_locations.txt"), ("platinum", "sinnoh_locations.txt"),
#         ("heartgold", "johto_locations.txt"), ("soulsilver", "johto_locations.txt"),]
#todo_games = [("black", "unova_locations.txt"), ("white", "unova_locations.txt"), ("black-2", "unova_locations.txt"),
#              ("white-2", "unova_locations.txt")]

dbkey = hidden.secrets()
update_evo_lines(table_names="gen_1_routes.txt", game_name="red", db_key=dbkey, pokedex_name="gen_1_dex")
#for g in todo_games:
#    lfile = g[0] + "_location_areas.txt"
#    createLocation_Area_Tables(location_areas_file=lfile, game_name=g[0], db_key=dbkey,
#                               gen_pokedex="gen_5_dex")