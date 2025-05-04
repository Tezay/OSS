import json
import os
from config import JSON_PLANET_DATA_PATH, DEFAULT_PLANET_TEXTURE_PATH, DIALOGUES_PATH, ITEMS_LIST_PATH, CRAFT_LIST_PATH


def get_planet_types():
    """
    Récupère tous les types de planètes avec leur taux d'apparition (spawn_rate) depuis le fichier planets.json.

    :return: Un dictionnaire où les clés sont les types de planètes et les valeurs leurs spawn_rate.
    """
    with open(JSON_PLANET_DATA_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return {planet["planet_type"]: planet["spawn_rate"] for planet in data["planets"]}

def get_planet_data(planet_type):
    """
    Récupère toutes les informations d'une planète à partir du fichier planets.json
    en fonction de son planet_type.

    :param planet_type: Le type de la planète (ex: 'desert', 'volcanic', 'ice')
    :return: Un dictionnaire contenant les informations de la planète, ou None si non trouvées
    """
    with open(JSON_PLANET_DATA_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    for planet in data["planets"]:
        if planet["planet_type"] == planet_type:
            return planet
    
    return None

def get_dialogues(dialogue_key):
    """
    Récupère une séquence de dialogues depuis le fichier dialogues.json
    en fonction de sa clé.

    :param dialogue_key: La clé de la séquence de dialogues (ex: 'initial_tutorial')
    :return: Une liste de chaînes de caractères (dialogues), ou None si non trouvée
    """
    try:
        with open(DIALOGUES_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get(dialogue_key)
    except FileNotFoundError:
        print(f"Error: Dialogues file not found at {DIALOGUES_PATH}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DIALOGUES_PATH}")
        return None

def get_items_data():
    """Charge les données des items depuis items_list.json."""
    try:
        with open(ITEMS_LIST_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {ITEMS_LIST_PATH} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error : Could not decode JSON from {ITEMS_LIST_PATH}.")
        return {}

def get_crafting_recipes():
    """Charge les recettes de craft depuis craft_list.json."""
    try:
        with open(CRAFT_LIST_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data["recipes"]
    except FileNotFoundError:
        print(f"Error : {CRAFT_LIST_PATH} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {CRAFT_LIST_PATH}.")
        return []