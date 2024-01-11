import requests
import json
from datetime import datetime

class PokemonOracle:

    def __init__(self):
        self.pokedex_url = "https://pokeapi.co/api/v2/pokedex/1/"
        self.pokedex = None
        self.total_num_pokemon = 0

    def load_pokedex(self):
        response = requests.get(self.pokedex_url)
        if response.status_code != 200:
            print("PokeAPI request failed: %s" % response.status_code)
            exit(1)

        self.pokedex = response.json()
        self.total_num_pokemon = len(self.pokedex['pokemon_entries'])

    def hash_to_pokemon(self, name, birthday, total_num_pokemon):
        str_to_hash = name + str(birthday)
        hash_value = sum(ord(char) for char in str_to_hash)
        pokemon_entry = hash_value % total_num_pokemon
        
        return pokemon_entry
    
    def get_spirit_pokemon(self, name, birthday):
        self.load_pokedex()

        pokemon_entry_num = self.hash_to_pokemon(name, birthday, self.total_num_pokemon)
        pokemon_entry = self.pokedex['pokemon_entries'][pokemon_entry_num - 1]

        request_url = 'https://pokeapi.co/api/v2/pokemon/' + pokemon_entry['pokemon_species']['name']
        response = requests.get(request_url)

        if response.status_code != 200:
            print("PokeAPI request failed: %s" % response.status_code)
            exit(1)

        pokemon = response.json()
        return pokemon['name']

if __name__ == "__main__":
    oracle = PokemonOracle()
    result = oracle.get_spirit_pokemon("Bob", datetime.strptime("01/01", "%m/%d"))
    print("Your spirit pokemon is " + result + ".")