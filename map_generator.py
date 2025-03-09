import random
import math

from config import (
    PLANET_MIN_DISTANCE,
    MAX_GENERATION_ATTEMPTS,
    PLANET_MIN_RADIUS,
    PLANET_MAX_RADIUS,
    PLANET_MIN_MASS,
    PLANET_MAX_MASS,
    PLANET_COLORS
)

class Planet:
    """
    Classe représentant une planète dans le monde.
    """
    def __init__(self, x, y, radius, mass, color):
        # Définir les caractéristiques d'une planète
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

    def __repr__(self):
        return f"Planet(x={self.x}, y={self.y}, radius={self.radius}, mass={self.mass})"


def generate_map(seed, world_width, world_height, number_of_planets=5):
    """
    Génère la map de façon déterministe en fonction de la seed.
    Retourne une liste de planètes (chaque planète est un objet de la classe Planet).
    """
    # Fixer la seed de la map
    random.seed(seed)

    planets = []

    for _ in range(number_of_planets):
        placed = False
        for attempt in range(MAX_GENERATION_ATTEMPTS):
            # Définir aléatoirement les coordonnées x, y de la planète
            x = random.randint(0, world_width)
            y = random.randint(0, world_height)
            # Définir aléatoirement la taille de la planète (rayon)
            radius = random.randint(PLANET_MIN_RADIUS, PLANET_MAX_RADIUS)
            # Définir aléatoirement la masse de la planète
            mass = random.uniform(PLANET_MIN_MASS, PLANET_MAX_MASS)
            # Définir aléatoirement la color de la planète (utilisation de texture à l'avenir)
            color = random.choice(PLANET_COLORS)

            # Vérifier la distance par rapport aux planètes déjà générées
            if can_place_planet(x, y, radius, planets, world_width, world_height):
                # Si la planète peut être placée, créer un nouvel objet planet avec les paramètres définis
                planet = Planet(x, y, radius, mass, color)
                # Ajouter cet objet à la liste des planètes
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
    et en évitant la zone de 400px autour du centre du monde.
    """
    # Définition du centre du monde
    center_x, center_y = world_width//2, world_height//2
    # Vérification de la distance par rapport au centre du monde
    if math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) < 400:
        return False
    
    # Vérification de la distance par rapport aux autres planètes
    for planet in existing_planets:
        dist_centers = math.sqrt((planet.x - x) ** 2 + (planet.y - y) ** 2)
        min_required = planet.radius + radius + PLANET_MIN_DISTANCE
        if dist_centers < min_required:
            return False
    
    return True
