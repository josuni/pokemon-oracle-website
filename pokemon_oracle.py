import requests
import json
from datetime import datetime

class PokemonOracle:

    def __init__(self):
        self.pokedex_url = 'https://pokeapi.co/api/v2/pokedex/1/' #national pokedex is used
        self.pokemon_entry_url_prefix = 'https://pokeapi.co/api/v2/pokemon/'
        self.pokedex = None
        self.total_num_pokemon = 0

    #sends request to PokeApi for pokedex data
    def load_pokedex(self):
        response = requests.get(self.pokedex_url)
        if response.status_code != 200:
            print("PokeAPI request failed when loading Pokedex: %s" % response.status_code)
            exit(1)

        self.pokedex = response.json()
        self.total_num_pokemon = len(self.pokedex['pokemon_entries'])
    
    #sends request to PokeApi for specific pokemon entry data
    def load_pokemon_entry(self, entry_num):
        pokemon_entry = self.pokedex['pokemon_entries'][entry_num - 1]

        request_url = self.pokemon_entry_url_prefix + pokemon_entry['pokemon_species']['name']
        response = requests.get(request_url)

        if response.status_code != 200:
            print("PokeAPI request failed when loading Pokemon Entry: %s" % response.status_code)
            exit(1)

        pokemon_data = response.json()
        return pokemon_data

    #hashes name + birthday string to bucket, number of buckets = length of pokedex
    def hash_to_pokemon(self, name, birthday, total_num_pokemon):
        str_to_hash = name + str(birthday)
        hash_value = sum(ord(char) for char in str_to_hash)
        pokemon_entry = hash_value % total_num_pokemon
        
        return pokemon_entry
    
    #driver code
    def get_spirit_pokemon(self, name, birthday):

        self.load_pokedex()

        pokemon_entry_num = self.hash_to_pokemon(name, birthday, self.total_num_pokemon)

        pokemon_data = self.load_pokemon_entry(pokemon_entry_num)
        pokemon_name, pokemon_image_url = pokemon_data['name'], pokemon_data['sprites']['front_default']
        
        return pokemon_name, pokemon_image_url

#example use and test code
if __name__ == "__main__":
    oracle = PokemonOracle()
    result = oracle.get_spirit_pokemon("Bob", datetime.strptime("01/01", "%m/%d"))
    print("Your spirit pokemon is " + result + ".")