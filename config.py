# Dimensions de la fenêtre
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Nombre d'images par seconde
FPS = 60

# Paramètre pour le mode debug
DEBUG_MODE = True

# Vitesse de déplacement de la caméra en mode debug
CAMERA_SPEED = 50

# Vaisseau
SPACESHIP_ROTATION_SPEED = 90 # degré/seconde
SPACESHIP_THRUST_FORCE = 1000 # force en Newton appliquée pendant l'appui
SPACESHIP_MAX_SPEED = 200
# Fichier de texture du vaisseau par défaut
SPACESHIP_TEXTURE_DEFAULT_PATH = "assets/spaceships/orange_spaceship.png"

# Dimensions de la map (grande carte pour l'exploration)
WORLD_WIDTH = 20000
WORLD_HEIGHT = 20000

# Paramètres de seed et de nombre de planètes
DEFAULT_SEED = None    # Si None, on génère une seed aléatoire.
custom_seed=None        #Si None, veux dire que l'uttilisateur n'a pas saisie de seed customisé
NUMBER_OF_PLANETS = 500  # Nombre de planètes à générer par défaut.

# --- Paramètres de distance pour la génération des planètes ---
PLANET_MIN_DISTANCE = 400       # Distance minimale entre les centres de deux planètes
MAX_GENERATION_ATTEMPTS = 200  # Nombre max de tentatives pour placer une planète

# --- Paramètres de caractéristiques des planètes ---
PLANET_MIN_RADIUS = 50
PLANET_MAX_RADIUS = 200
PLANET_MIN_MASS = 1e4
PLANET_MAX_MASS = 1e6

# On définit un set de colors possibles pour les planètes
PLANET_COLORS = [
    (255, 0, 0),      # Rouge
    (0, 255, 0),      # Vert
    (0, 0, 255),      # Bleu
    (255, 255, 0),    # Jaune
    (255, 165, 0),    # Orange
    (255, 192, 203),  # Rose
    (128, 0, 128),    # Violet
    (0, 255, 255),    # Cyan
    (139, 69, 19),    # Marron
    (75, 0, 130),     # Indigo
    (218, 112, 214),  # Orchidée
    (0, 128, 128),    # Sarcelle
    (154, 205, 50),   # Vert jaune
    (128, 128, 128),  # Gris
]

import pygame
# Dictionnaire des bindings (actions -> touches)
KEY_BINDINGS = {
    "camera_left": pygame.K_LEFT,
    "camera_right": pygame.K_RIGHT,
    "camera_up": pygame.K_UP,
    "camera_down": pygame.K_DOWN,
    "zoom_in": pygame.K_z,
    "zoom_out": pygame.K_x,
    "pause": pygame.K_p,       # Touche pour basculer en pause
    "start_game": pygame.K_RETURN, # Touche pour lancer la partie depuis le menu
    # Touches de tests déplacement vaisseau :
    "spaceship_move": pygame.K_SPACE, # Touche test pour faire avancer le vaisseau
    "spaceship_deceleration": pygame.K_RSHIFT, # Touche test pour faire décélérer le vaisseau
    "spaceship_stop": pygame.K_0, # Touche test pour arrêter le mouvement du vaisseau
    "spaceship_rotate_left": pygame.K_q,
    "spaceship_rotate_right": pygame.K_d
}

# Taille des boutons (globales, afin de pouvoir les éditer dynamiquement pendant l'exécution du jeu)
global button_size_widht,button_size_height 
button_size_widht = WINDOW_WIDTH * 0.2  # Largeur : 20% de la largeur de la fenêtre
button_size_height = WINDOW_HEIGHT * 0.1  # Hauteur : 10% de la hauteur de la fenêtre