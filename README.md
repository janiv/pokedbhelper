This repository was built as a CLI tool to create local postgres Pokemon related databases. I am using this repository to help create the databases and tables I need for a personal project.
The personal project is a Pokemon fansite that where users can play a modified Nuzlocke challenge. I call it a Fateslocke. Your Nuzlocke encounters are rolled ahead of time. To create the 
fanwebsite, and to teach myself about web development I needed this tool to access pokeapi.co and to create useful databases for each game.

The main things this tool can do are:
  1.Create a local pokedex in a postgres db with the following columns:
    id  name  type_1  type_2  evo_id

  The first 4 are self explanatory, evo_id is the evolutionary line id. So Bulbasaur, Ivysaur, and Venusaur are all 1. Charmander, Charmeleon, Charizard are 2 and so on.
  The evo_id is there so that I can create a Nuzlocke encounter roller with dupes clause enabled.

  2. Create encounter tables in a postgres db with the following columns:
      id enc_method
     So for Pokemon Red it would create a table called "Route_1" with entries "Pidgey_id walk" and "Rattata_id walk". It would do so for all locations in Pokemon Red.

  3. It can also create a location_areas_table that contains all location areas where the player may encounter new pokemon.
