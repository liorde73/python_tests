import pytest
import requests
import json

test_Api_URI = "https://pokeapi.co/api/v2/type"
Pokemon_Cnt = 20

# STEP - 1:
# Retrieve values from valid URL and verify correct Pokemon amount is returned
# ---------
response = requests.get(test_Api_URI) # get the data from the URL
response.raise_for_status() # assert if there was an error with this request

print(f"Response.text = {response.text}")
resp_json = json.loads(response.content.decode('utf-8')) # used for easier handling

# validate correct amount of Pokemons
assert resp_json['count'] == Pokemon_Cnt , f"'Count' of Pokemons should be {Pokemon_Cnt} Instead, it is : {resp_json['count']}"

# another way to validate the number of Pokemon-types
assert len(resp_json['results']) == Pokemon_Cnt, f"Amount of Pokemons-RESULTS should be {Pokemon_Cnt} Instead, it is : {len(resp_json['results'])}"


# STEP - 2:
# Discover ID of the Fire-Type Pokemnons and verify 2 names
# ---------
poke_fire_type_url = ""
for poke_type in resp_json['results']:
    print(poke_type) # for debugging...
    if poke_type['name'].upper() == "FIRE": # compare to upper case to avoid future possible Typo's
        poke_fire_type_url = poke_type['url']
        print(f"Fire-type url is : {poke_fire_type_url}")
        break

assert poke_fire_type_url != "", f"Failed to find a URL for the 'fire' type Pokemon."

poke_present = 'charmander'
poke_absent = 'bulbasaur'

response_fireType = requests.get(poke_fire_type_url) # get the data from the URL
response_fireType.raise_for_status() # assert if there was an error with this request

print(f"Response.text = {response_fireType.text}") # just for debugging...
resp_json_fireType = json.loads(response_fireType.content.decode('utf-8')) # used for easier handling

# verify the this pokemon IS in the list
poke_present_val = poke_present in response_fireType.text  # should be 'True'
assert poke_present_val == True , f"Pokemon '{poke_present}' should BE present in the FireType Pokemons list. "

# verify the this pokemon IS NOT in the list
poke_absent_val = poke_absent not in response_fireType.text  # should be 'False'
assert poke_absent_val == True , f"Pokemon '{poke_absent}' should NOT BE present in the FireType Pokemons list. "


# STEP - 3:
# Identify 5 heaviest Pokemons of type Fire and verify weights.
# ---------
dict_Fire_HeavyWeight = {"charizard-gmax": 10000, 
                        "cinderace-gmax": 10000,
                        "coalossal-gmax": 10000,
                        "centiskorch-gmax": 10000,
                        "groudon-primal": 9997}

# iterate over the 5 heavyweights and search for them in the main results
for poke_name in dict_Fire_HeavyWeight.keys():
    print(f"Pokemon name in dictionary is: '{poke_name}'")
    poke_weight = dict_Fire_HeavyWeight[poke_name]
    print(f"Pokemon weight in dictionary is: '{poke_weight}'")
    
    # search each heavyweight Pokemon, in the Json and verify it's weight through it's **relevant url**
    for json_poke_name in resp_json_fireType['pokemon']:
        print(f"'json_poke_name' is : {json_poke_name}") # for debugging
        # if this pokemon is the one from the dictionary then continue checking it's weight
        if json_poke_name['pokemon']['name'] == poke_name:
            print(f"Pokemon's name is : {json_poke_name['pokemon']['name']}")
            heavy_pokemonURL = ""
            heavy_pokemonURL = json_poke_name['pokemon']['url']
            print(f"Heavy Pokemon url is : '{heavy_pokemonURL}'")
            response_heavyweight = ""
            response_heavyweight = requests.get(heavy_pokemonURL) # get the data from the URL
            response_heavyweight.raise_for_status() # assert if there was an error with this request

            #print(f"response_heavyweight.text = {response_heavyweight.text}") # just for debugging...
            resp_json_heavyweight = ""
            resp_json_heavyweight= json.loads(response_heavyweight.content.decode('utf-8')) # used for easier handling
            current_weight = resp_json_heavyweight['weight']
            print(f"Pokemon: {json_poke_name['pokemon']['name']} weight is: {str(current_weight)}")
            assert resp_json_heavyweight['weight'] == poke_weight, f"Weight mismatch!! Pokemon '{poke_name} expected weight is: {poke_weight}. Instead found weight of: {resp_json_heavyweight['weight']} !"

