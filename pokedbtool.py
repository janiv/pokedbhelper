from hidden import secrets
import pokedexdbmaker
from locationsmaker import findLocations, findLocationAreasURL
from locationsmaker import createLocation_Area_Tables

def db_access(db: str):
    db_key = secrets()
    db_key["database"] = db
    return db_key


def pokedex_db_maker(poke_gen: str, max_id_val: int):
    pokedex_db_key = db_access(poke_gen)
    pokedexdbmaker.pokedexHelper(file_name=poke_gen, min_id=1,
                                 max_id=max_id_val, secrets=pokedex_db_key)


def encounter_db_maker(poke_gen: str, game_name: str, game_area_id: int):
    pokedex_db_key = db_access(poke_gen)
    locations_db_key = db_access(game_name)
    locations_file = findLocations(gameName=game_name, id = game_area_id)
    location_area_file = findLocationAreasURL(gameName=game_name,
                                              location_file_name=locations_file)
    createLocation_Area_Tables(location_areas_file=location_area_file,
                               game_name= game_name, loc_db_key= locations_db_key,
                               pokedex_db_key= pokedex_db_key)


games = [["gen_1_pokedex", "blue", 1]]
for g in games:
    encounter_db_maker(poke_gen=g[0], game_name=g[1], game_area_id=g[2])