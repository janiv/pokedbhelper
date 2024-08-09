from hidden import secrets
import pokedexdbmaker


def db_access(db: str):
    db_key = secrets()
    db_key["database"] = db
    return db_key


def pokedex_db_maker(poke_gen: str, max_id_val: int):
    pokedex_db_key = db_access(poke_gen)
    pokedexdbmaker.pokedexHelper(file_name=poke_gen, min_id=1, max_id=max_id_val,
                                 secrets=pokedex_db_key)


gens_list = [["gen_3_pokedex", 386]]
for gen in gens_list:
    pokedex_db_maker(gen[0], gen[1])
