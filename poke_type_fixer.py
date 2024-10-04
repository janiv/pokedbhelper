import requests
import psycopg2
from psycopg2 import sql
from hidden import secrets

gen_1 = {
    "clefairy": ("normal", None),
    "clefable": ("normal", None),
    "jigglypuff": ("normal", None),
    "wigglytuff": ("normal", None),
    "magnemite" : ("electric", None),
    "magneton" : ("electric", None),
    "mr-mime": ("psychic", None)
}


gen_2 = {
    "clefairy": ("normal", None),
    "clefable": ("normal", None),
    "jigglypuff": ("normal", None),
    "wigglytuff": ("normal", None),
    "mr-mime": ("psychic", None),
    "cleffa": ("normal", None),
    "igglybuff": ("normal", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "marill": ("water", None),
    "azumarill": ("water", None),
    "snubbull": ("normal", None),
    "granbull": ("normal", None)
}

gen_3 = {
    "clefairy": ("normal", None),
    "clefable": ("normal", None),
    "jigglypuff": ("normal", None),
    "wigglytuff": ("normal", None),
    "mr-mime": ("psychic", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "snubbull": ("normal", None),
    "granbull": ("normal", None),
    "cleffa": ("normal", None),
    "igglybuff": ("normal", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "marill": ("water", None),
    "azumarill": ("water", None),
    "ralts": ("psychic", None),
    "kirlia": ("psychic", None),
    "gardevoir": ("psychic", None),
    "azurill": ("normal", None),
    "mawile": ("steel", None)
}

gen_4 = {
    "clefairy": ("normal", None),
    "clefable": ("normal", None),
    "jigglypuff": ("normal", None),
    "wigglytuff": ("normal", None),
    "mr-mime": ("psychic", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "snubbull": ("normal", None),
    "granbull": ("normal", None),
    "cleffa": ("normal", None),
    "igglybuff": ("normal", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "marill": ("water", None),
    "azumarill": ("water", None),
    "ralts": ("psychic", None),
    "kirlia": ("psychic", None),
    "gardevoir": ("psychic", None),
    "azurill": ("normal", None),
    "mawile": ("steel", None),
    "mime-jr": ("psychic", None),
    "togekiss": ("normal", "flying")
}

gen_5 = {
    "clefairy": ("normal", None),
    "clefable": ("normal", None),
    "jigglypuff": ("normal", None),
    "wigglytuff": ("normal", None),
    "mr-mime": ("psychic", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "snubbull": ("normal", None),
    "granbull": ("normal", None),
    "cleffa": ("normal", None),
    "igglybuff": ("normal", None),
    "togepi": ("normal", None),
    "togetic": ("normal", "flying"),
    "marill": ("water", None),
    "azumarill": ("water", None),
    "ralts": ("psychic", None),
    "kirlia": ("psychic", None),
    "gardevoir": ("psychic", None),
    "azurill": ("normal", None),
    "mawile": ("steel", None),
    "mime-jr": ("psychic", None),
    "togekiss": ("normal", "flying"),
    "cottonee": ("grass", None),
    "whimsicott": ("grass", None)
}

def pokedex_updater(pokedex: str, db_key: dict, corrections: dict):
    db_info = db_key
    conn = psycopg2.connect(database=db_info['database'],
                            user=db_info['user'],
                            host=db_info['host'],
                            password=db_info['password'],
                            port=db_info['port'])
    cur = conn.cursor()
    for k,v in corrections.items():
        name = k
        type_1 = v[0]
        type_2 = v[1]
        cur.execute(sql.SQL("""UPDATE {} SET poke_type_1=%s, poke_type_2=%s 
                            WHERE poke_name=%s;""")
                            .format(sql.Identifier(f'{pokedex}')),
                            (type_1, type_2, name))
    conn.commit()
    cur.close()
    conn.close()


db_key = secrets()
gens = [ ("gen_1_dex", gen_1), ("gen_2_dex", gen_2), ("gen_3_dex", gen_3),
        ("gen_4_dex", gen_4), ("gen_5_dex", gen_5)]
for gen in gens:
    pokedex_updater(gen[0], db_key, gen[1])