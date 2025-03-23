import json

from config import JSON_PLANET_DATA_PATH


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