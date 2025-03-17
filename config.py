import pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Nombre d'images par seconde
FPS = 100

# Paramètre pour le mode debug
DEBUG_MODE = False

# Vitesse de déplacement de la caméra en mode debug
CAMERA_SPEED = 50

# Distance de rendu autour du vaisseau (rayon, en pixels)
RENDER_DISTANCE = WINDOW_WIDTH + 100

# Vaisseau
SPACESHIP_ROTATION_SPEED = 90 # degré/seconde
SPACESHIP_THRUST_FORCE = 1000 # force en Newton appliquée pendant l'appui
SPACESHIP_MAX_SPEED = 200
SPACESHIP_MASS = 40
# Fichier de texture du vaisseau par défaut
SPACESHIP_TEXTURE_DEFAULT_PATH = "assets/spaceships/orange_spaceship.png"

########### Configuration de l'écran et de la police ############
# Font path
FONT_PATH = "assets/fonts/Retro_Gaming.ttf"
DEFAULT_FONT_SIZE = 24

try:
    custom_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)  # Police chargée une seule fois
except:
    print(f"Impossible to load {FONT_PATH} font, default font loaded.")
    custom_font = pygame.font.SysFont("Arial", DEFAULT_FONT_SIZE)

# Configuration de l'écran
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
##################################################################

# Fichier de données locales par défaut
LOCAL_DATA_PATH = "local_data/"
TECH_TREE_DEFAULT_DATA_PATH = "data/tech_tree_data.json"
TECH_TREE_TEMPLATE_PATH = "data/tech_tree_session_template.json"

# Inventaire par défaut (exemple d'inventaire)
DEFAULT_INVENTORY = {"items": [{"name": "water", "quantity": 5}]}

# Dimensions de la map (grande carte pour l'exploration)
WORLD_WIDTH = 20000
WORLD_HEIGHT = 20000

# Paramètres de seed et de nombre de planètes
DEFAULT_SEED = None    # Si None, on génère une seed aléatoire.
custom_seed=None        #Si None, veux dire que l'uttilisateur n'a pas saisie de seed customisé
NUMBER_OF_PLANETS = 250  # Nombre de planètes à générer par défaut.

# Paramètres de distance pour la génération des planètes
PLANET_MIN_DISTANCE = 800       # Distance minimale entre les centres de deux planètes
MAX_GENERATION_ATTEMPTS = 200  # Nombre max de tentatives pour placer une planète

# Constante de gravitation
G = 4

# Vitesse maximum d'atterrisage
MAX_LANDING_SPEED = 40

# Planètes
DEFAULT_PLANET_TEXTURE_PATH = "assets/planets/"
JSON_PLANET_DATA_PATH = "data/planets.json"


import pygame
# Dictionnaire des bindings (actions -> touches)
KEY_BINDINGS = {
    "camera_left": pygame.K_LEFT,
    "camera_right": pygame.K_RIGHT,
    "camera_up": pygame.K_UP,
    "camera_down": pygame.K_DOWN,
    "zoom_in": pygame.K_z,
    "zoom_out": pygame.K_x,
    "inventory": pygame.K_i,       # Touche pour basculer en pause
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



# dictionaire des boutons
# sous la forme {"nom button":{
#                             "x":position x,"y":position y,"button_size_widht":taille button,"button_size_height":hauteur button
#                             "color":couleur,"text": texte dans le button,"file":fichier pour l'image}}
buttons={
    "tech_tree":{
        "x":31,"y":30,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Abre technologique","file":"assets/button.png"},

    "resolution_menu_screen":{
        "x":20,"y":20,"button_size_widht":button_size_widht,"button_size_height":button_size_height,""
        "color":(255,255,255),"text":"Résolution","file":"assets/button.png"},

    "resolution_game_screen":{
        "x":20,"y":20,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Résolution","file":"assets/button.png"},

    "launch":{
        "x":2,"y":10,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Lancer le jeu","file":"assets/button.png"},

    "menu_settings":{
        "x":2,"y":20,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Paramètres","file":"assets/button.png"},

    "game_settings":{
        "x":15,"y":30,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Paramètres","file":"assets/button.png"},

    "quit":{
        "x":2,"y":30,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Quitter le jeu","file":"assets/button.png"},

    "return":{
        "x":10,"y":25,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Retour","file":"assets/button.png"},

    "full_screen":{
        "x":25,"y":10,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Plein écran","file":"assets/button.png"},

    "resolution_1280x720":{
        "x":25,"y":15,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"1280x720","file":"assets/button.png"},

    "resolution_1920x1080":{
        "x":25,"y":20,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"1920x1080","file":"assets/button.png"},

    "resolution_1920x1200":{
        "x":25,"y":25,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"1920x1200","file":"assets/button.png"},

    "resolution_2560x1080":{
        "x":25,"y":30,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"2560x1080","file":"assets/button.png"},

    "seed":{
        "x":10,"y":10,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Seed","file":"assets/button.png"},

    "return_menu":{
        "x":30,"y":30,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Retour au menu","file":"assets/button.png"},

    # Bouton pour tester l'upgrade de module de tier dans l'arbre technologique
    "test_upgrade_tech_tree_module":{
        "x":30,"y":30,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Bouton test pour upgrade tier module tech tree","file":"assets/button.png"},

    "test_add_item":{
        "x":30,"y":20,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Bouton test pour ajouter un item","file":"assets/button.png"},

    "test_remove_item":{
        "x":30,"y":25,"button_size_widht":button_size_widht,"button_size_height":button_size_height,
        "color":(255,255,255),"text":"Bouton test pour retirer un item","file":"assets/button.png"},
}