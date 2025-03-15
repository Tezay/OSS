import random
import math
import pygame
import os

from json_manager import get_planet_types, get_planet_data
from config import PLANET_MIN_DISTANCE, MAX_GENERATION_ATTEMPTS, DEFAULT_PLANET_TEXTURE_PATH

# Dictionnaire pour cacher/mettre en mémoire les images
PLANET_IMAGE_CACHE = {}

class Planet:
    """
    Classe représentant une planète dans le monde.
    """
    def __init__(self, x, y, radius, mass, texture, planet_type):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        # Nom de la texture
        self.texture = texture
        # Chemin d'accès de la texture
        self.texture_path = os.path.join(DEFAULT_PLANET_TEXTURE_PATH, f"{self.texture}.png")

        self.planet_type = planet_type

        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = (x, y)
        
    def draw(self, world_surface):
        """
        Dessine la planète en tenant compte de la caméra (pour le décalage).
        """
        # Charger l'image de la texture
        planet_image = pygame.image.load(self.texture_path).convert_alpha()
        planet_image = pygame.transform.scale(
            planet_image, 
            (self.radius*2, self.radius*2)
        )

        # On calcule un rect dont le center est (self.x, self.y)
        draw_rect = planet_image.get_rect()
        draw_rect.center = (self.x, self.y)

        # Blit dans la surface world
        world_surface.blit(planet_image, draw_rect)

    # Méthode pour renvoyer tous les attribus d'une planète
    def __repr__(self):
        return (f"Planet(x={self.x}, y={self.y}, radius={self.radius}, mass={self.mass}, texture={self.texture}, type={self.planet_type})")


def generate_map(seed, world_width, world_height, number_of_planets=5):
    """
    Génère la map de façon déterministe en fonction de la seed,
    en se basant sur les données JSON récupérées par get_planet_data.
    
    Retourne une liste de planètes (chaque planète est un objet de la classe Planet).
    """
    # Spécifie la seed utilisée au module random
    random.seed(seed)

    # Initialise une liste vide qui contiendra les planètess
    planets = []
    
     # Récupération des types de planètes et de leur spawn_rate
    planet_types = get_planet_types()
    # Création de la liste vide
    # Note : La fréquence d'apparition d'un type de planète correspond à sa probabilité de génération
    weighted_planet_types = []

    # Création d'une liste pondérée
    for planet_type, spawn_rate in planet_types.items():
        weighted_planet_types.extend([planet_type] * spawn_rate)

    # Itération sur chaque planète
    for _ in range(number_of_planets):
        placed = False
        # Essayer de placer la planète autant de fois que possible
        for attempt in range(MAX_GENERATION_ATTEMPTS):
            # Choisir un planet_type au hasard dans ta liste possible
            planet_type = random.choice(weighted_planet_types)
            # Récupérer la config de cette planète depuis le fichier JSON
            planet_data = get_planet_data(planet_type)
            if not planet_data:
                # Si jamais la planète n'est pas trouvée dans le JSON, on saute
                print("Specified planet type not finded in json file.")
                continue
            
            # Définir aléatoirement les coordonnées x, y de la planète
            x = random.randint(0, world_width)
            y = random.randint(0, world_height)
            
            # Définir le rayon et la masse en se basant sur le min et max du JSON
            # Note : Conversion des min_mass/max_mass en float avant d’appeler random.uniform
            radius = random.randint(planet_data["min_radius"], planet_data["max_radius"])
            mass = random.uniform(float(planet_data["min_mass"]), float(planet_data["max_mass"]))
            
            # Choisir une texture aléatoire parmi la liste de textures disponibles
            texture = "default"
            if planet_data["texture"]:
                texture = random.choice(planet_data["texture"])

            # Vérifier si la planète peut être placée
            if can_place_planet(x, y, radius, planets, world_width, world_height):
                # Créer l’objet Planet
                planet = Planet(x, y, radius, mass, texture, planet_type)
                planets.append(planet)
                placed = True
                break
        
        if not placed:
            print("Warning: Impossible to place a supplementary planet.")

    return planets


def can_place_planet(x, y, radius, existing_planets, world_width, world_height):
    """
    Vérifie si on peut placer une nouvelle planète (x, y, radius)
    en respectant la distance minimale par rapport aux planètes existantes
    et en évitant la zone de PLANET_MIN_DISTANCE autour du centre du monde.
    """
    # Définition du centre du monde
    center_x, center_y = world_width//2, world_height//2
    # Vérification de la distance par rapport au centre du monde
    if math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) < PLANET_MIN_DISTANCE:
        return False
    
    # Vérification de la distance par rapport aux autres planètes
    for planet in existing_planets:
        dist_centers = math.sqrt((planet.x - x) ** 2 + (planet.y - y) ** 2)
        min_required = planet.radius + radius + PLANET_MIN_DISTANCE
        if dist_centers < min_required:
            return False
    
    return True
