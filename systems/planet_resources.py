import os
import json
import pygame
from config import ITEMS_LIST_PATH

def load_item_images(scale_size=(32, 32)):
    """
    Charge les images des items depuis items_list.json et les redimensionne.

    :param scale_size: Tuple (width, height) pour redimensionner les images.
    :return: Un dictionnaire où les clés sont les noms des items (item_key)
             et les valeurs sont les surfaces Pygame des images chargées et redimensionnées.
    """
    item_images = {}
    try:
        with open(ITEMS_LIST_PATH, 'r', encoding='utf-8') as file:
            items_data = json.load(file)
            for item_key, item_info in items_data.items():
                texture_path = item_info.get("texture")
                if texture_path and os.path.exists(texture_path):
                    try:
                        # Charger l'image
                        img = pygame.image.load(texture_path).convert_alpha()
                        # Redimensionner l'image
                        item_images[item_key] = pygame.transform.scale(img, scale_size)
                    except pygame.error as e:
                        print(f"Error loading or scaling image for item '{item_key}' at path '{texture_path}': {e}")
                else:
                    print(f"Warning: Texture not found or path invalid for item '{item_key}' at path '{texture_path}'")
    except FileNotFoundError:
        print(f"Error: {ITEMS_LIST_PATH} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {ITEMS_LIST_PATH}.")
    except Exception as e:
        print(f"An unexpected error occurred while loading item images: {e}")
    return item_images

def collect_planet_resources(planet, inventory):
    """
    Transfère toutes les ressources de la planète vers l'inventaire et réinitialise
    les ressources de la planète à zéro.

    :param planet: L'objet Planet dont les ressources doivent être collectées.
    :param inventory: L'objet Inventory du joueur.
    """
    if not planet or not inventory:
        print("Error: Planet or Inventory object is missing.")
        return

    items_collected = {}
    # Itération à travers une copie des items pour éviter les problèmes de modifications
    for resource_name, quantity in list(planet.resources.items()):
        # Vérifie si la ressource existe dans l'inventaire
        if quantity > 0:
            # Ajoute la ressource à l'inventaire
            inventory.add_item(resource_name, quantity)
            items_collected[resource_name] = quantity
            # Réinitialise la ressource sur la planète
            planet.resources[resource_name] = 0.0

    # Vérifie si des ressources ont été collectées
    if items_collected:
        print(f"Collected resources from {planet.name}: {items_collected}")
    else:
        print(f"No resources to collect from {planet.name}.")
