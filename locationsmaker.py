import hidden
import requests
import psycopg2
from psycopg2 import sql
from typing import List


secrets = hidden.secrets()


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


def findLocationAreasURL(gameName: str, location_file_name: str):
    # We need to write code such that for each location we go to all location
    # areas, and write them to a txt file.
    f = open(location_file_name, 'r')
    data = f.readlines()
    f.close()
    loc_area_f = open(gameName+"_location_areas.txt", "w")
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


def getID(poke_name: str) -> str:
    db_info = secrets
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["pass"],
                            port=db_info['port'])
    cur = conn.cursor()
    query = "SELECT id FROM pokedex where poke_name = %s;"
    cur.execute(query, (poke_name,))
    result = cur.fetchone()
    return result


def createDB(location_area_name: str, pokes: List[str], methods: List[str]):
    db_info = secrets
    conn = psycopg2.connect(database=db_info["database"],
                            user=db_info["user"],
                            host=db_info['host'],
                            password=db_info["pass"],
                            port=db_info['port'])
    cur = conn.cursor()
    print("Attempting to create: " + location_area_name)
    area_name = location_area_name.strip()
    cur.execute(sql.SQL("""CREATE TABLE IF NOT EXISTS {} (
                    poke_id integer NOT NULL PRIMARY KEY,
                    pokemon VARCHAR (30) NOT NULL,
                    encounter_method VARCHAR(15) NOT NULL);""")
                .format(sql.Identifier(f'{area_name}')))
    for i in range(len(pokes)):
        id = getID(pokes[i])[0]
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


def createLocation_Area_Tables(location_areas_file: str, game_name: str):
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
            response = requests.get(url)
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
        table_name = table_name.replace("-", "_")
        createDB(table_name, valid_pokes, encounter_methods)


createLocation_Area_Tables("red_location_areas.txt", "red")