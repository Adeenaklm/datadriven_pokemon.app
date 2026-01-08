import requests

BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon(name_or_id):
    url = f"{BASE_URL}/pokemon/{name_or_id.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    pokemon_data = {
        "name": data["name"].title(),
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"].title() for t in data["types"]],
        "abilities": [a["ability"]["name"].title() for a in data["abilities"]],
        "stats": {
            stat["stat"]["name"].upper(): stat["base_stat"]
            for stat in data["stats"]
        },
        "sprite": data["sprites"]["front_default"]
    }

    return pokemon_data

def get_pokemon_by_type(type_name):
    """
    Fetch a list of Pokémon names that belong to a specific type.
    """
    url = f"{BASE_URL}/type/{type_name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    return [p["pokemon"]["name"] for p in data["pokemon"]]

    