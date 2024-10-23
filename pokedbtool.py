from hidden import secrets
import pokedexdbmaker
import psycopg2;
from psycopg2 import sql;
from locationsmaker import findLocations, findLocationAreasURL
from locationsmaker import createLocation_Area_Tables


def pokedex_db_maker(poke_gen: str, max_id_val: int):
    poke_db_key = secrets()
    pokedexdbmaker.pokedexHelper(file_name=poke_gen, min_id=1,
                                 max_id=max_id_val, secrets=poke_db_key)


def encounter_db_maker(poke_gen: str, game_name: str, game_area_id: int,
                       gen_pokedex: str):
    db_key = secrets()
    locations_file = findLocations(gameName=game_name, id=game_area_id)
    location_area_file = findLocationAreasURL(gameName=game_name,
                                              location_file_name=locations_file
                                              )
    createLocation_Area_Tables(location_areas_file=location_area_file,
                               game_name=game_name, db_key=db_key,
                               gen_pokedex=gen_pokedex)
