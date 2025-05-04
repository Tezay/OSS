import pygame
pygame.init()

# ----------------------------- CONFIGURATION GÉNÉRALE -----------------------------
# Dimensions de la fenêtre 
WINDOW_WIDTH = 1280  # Largeur de la fenêtre en pixels
WINDOW_HEIGHT = 720  # Hauteur de la fenêtre en pixels

# Nombre d'images par seconde 
FPS = 50  # Framerate cible du jeu

# Mode debug 
DEBUG_MODE = False  # Active ou désactive le mode debug

# ----------------------------- PARAMÈTRES DU VAISSEAU -----------------------------
# Rotation et vitesse du vaisseau 
SPACESHIP_ROTATION_SPEED = 90  # Vitesse de rotation en degrés par seconde
SPACESHIP_THRUST_FORCE = 600  # Force de poussée en Newton
SPACESHIP_MAX_SPEED = 100  # Vitesse maximale du vaisseau
SPACESHIP_MASS = 40  # Masse du vaisseau en unités arbitraires
SPACESHIP_MAX_PROPELLANT = 50  # Quantité maximale de propergol
SPACESHIP_MAX_NITROGEN = 20  # Quantité maximale de nitrogène

# Texture par défaut du vaisseau 
SPACESHIP_TEXTURE_DEFAULT_PATH = "assets/spaceships/orange_spaceship.png"

# ----------------------------- PARAMÈTRES DE LA GRAVITÉ -----------------------------
# Constante gravitationnelle 
G = 4  # Constante de gravitation utilisée dans les calculs physiques

# ----------------------------- PARAMÈTRES DE L'ATTERRISSAGE -----------------------------
# Coefficient de rebond lors de l'atterrissage 
LANDING_DAMPING_FACTOR = 0.2  # Coeff de vitesse transmise au rebond lors de l'atterrissage

# Vitesse maximale d'atterrissage 
MAX_LANDING_SPEED = 20  # Vitesse maximale autorisée pour un atterrissage réussi

# ----------------------------- PARAMÈTRES DE LA MAP -----------------------------
# Dimensions de la map
WORLD_WIDTH = 15000  # Largeur de la map en pixels
WORLD_HEIGHT = 15000  # Hauteur de la map en pixels

# Seed par défaut pour la génération procédurale 
DEFAULT_SEED = None  # None pour une seed aléatoire

# Densité des planètes 
PLANET_DENSITY = 0.0000006  # Nombre de planètes par pixel carré

# Distance minimale entre les planètes 
PLANET_MIN_DISTANCE = 800  # Distance minimale entre les centres de deux planètes

# Nombre maximum de tentatives pour placer une planète 
MAX_GENERATION_ATTEMPTS = 200  # Tentatives avant d'abandonner la génération d'une planète

# ----------------------------- PARAMÈTRES DES ÉTOILES -----------------------------
# Densité des étoiles
STAR_DENSITY = 0.00005  # Nombre d'étoiles par pixel carré

# Tailles possibles des étoiles
STAR_SIZES = [1, 2, 3, 4, 5]  # Tailles en pixels

# Couleurs possibles des étoiles
STAR_COLORS = [
    (255, 255, 255),  # Blanc
    (200, 200, 255),  # Bleu clair
    (255, 200, 200),  # Rose clair
    (255, 255, 200),  # Jaune clair
]

# ----------------------------- PARAMÈTRES DE L'INVENTAIRE -----------------------------
# Inventaire par défaut
DEFAULT_INVENTORY = {
    "items": [
        {"name": "iron_ore", "quantity": 1},
        {"name": "azure_crystals", "quantity": 1},
        {"name": "organic_fibers", "quantity": 1},
        {"name": "hydrogen_gas", "quantity": 1},
        {"name": "neutral_gas", "quantity": 1},
        {"name": "compressed_carbon", "quantity": 1},
        {"name": "raw_silicon", "quantity": 1},
        {"name": "stellar_dust", "quantity": 1},
        {"name": "luminous_lithium", "quantity": 1},
        {"name": "volcanic_plasma", "quantity": 1},
        {"name": "frozen_water", "quantity": 1},
        {"name": "liquid_water", "quantity": 1},
        {"name": "antimatter", "quantity": 1},
        {"name": "mines", "quantity": 10}
    ]
}

# ----------------------------- PARAMÈTRES DE L'INTERFACE -----------------------------
# Police par défaut
FONT_PATH = "assets/fonts/Retro_Gaming.ttf"  # Chemin vers la police
DEFAULT_FONT_SIZE = 24  # Taille de la police par défaut
DIRECTIONAL_ARROW_TEXTURE_PATH = "assets/directional_arrow.png"  # Texture de la flèche directionnelle

# Taille des boutons

button_size_widht = 12  # Largeur : 20% de la largeur de la fenêtre
button_size_height = 4  # Hauteur : 10% de la hauteur de la fenêtre


# ----------------------------- PARAMÈTRES DE RENDU -----------------------------
# Distance de rendu autour du vaisseau
if DEBUG_MODE==True:
    RENDER_DISTANCE = WINDOW_WIDTH * 10  # Rayon en pixels
else:
        RENDER_DISTANCE = WINDOW_WIDTH * 2  # Rayon en pixels


# ----------------------------- PARAMÈTRES DE LA CAMÉRA -----------------------------
# Vitesse de déplacement de la caméra en mode debug
CAMERA_SPEED = 50  # Vitesse de déplacement en pixels par frame

# ----------------------------- PARAMÈTRES DES BINDINGS -----------------------------
# Dictionnaire des bindings
KEY_BINDINGS = {
    "camera_left": pygame.K_LEFT,
    "camera_right": pygame.K_RIGHT,
    "camera_up": pygame.K_UP,
    "camera_down": pygame.K_DOWN,
    "zoom_in": pygame.K_z,
    "zoom_out": pygame.K_x,
    "inventory": pygame.K_i,
    "game_over": pygame.K_g,
    "start_game": pygame.K_RETURN,
    "spaceship_move": pygame.K_SPACE,
    "spaceship_deceleration": pygame.K_RSHIFT,
    "spaceship_stop": pygame.K_0,
    "spaceship_rotate_left": pygame.K_q,
    "spaceship_rotate_right": pygame.K_d,
    "exit_current_menu" : pygame.K_ESCAPE,
    "open_map" : pygame.K_m,
}


# ----------------------------- CHEMINS DES FICHIERS -----------------------------
# Chemins des fichiers de données
LOCAL_DATA_PATH = "local_data/"
TECH_TREE_DEFAULT_DATA_PATH = "data/tech_tree_data.json"
TECH_TREE_TEMPLATE_PATH = "data/tech_tree_session_template.json"
DEFAULT_PLANET_TEXTURE_PATH = "assets/planets/"
JSON_PLANET_DATA_PATH = "data/planets.json"
ITEMS_LIST_PATH = "data/items_list.json"
HUD_TEXTURE_PATH = "assets/hud/"
DIALOGUES_PATH = "data/dialogues.json"


# ----------------------------- VARIABLES INTERNES (NE PAS MODIFIER) -----------------------------
# Ne surtout pas modifier, variables nécessaires au fonctionnement du jeu

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

respawning = False  # Indique si le joueur est en train de respawn
custom_seed = None  # Stocke la seed personnalisée

tech_button_size_widht = button_size_widht // 2  # Largeur des boutons tech
tech_button_size_height = button_size_height // 2  # Hauteur des boutons tech

# Chargement de la police (ne pas modifier)
try:
    custom_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)
except:
    print(f"Impossible to load {FONT_PATH} font, default font loaded.")
    custom_font = pygame.font.SysFont("Arial", DEFAULT_FONT_SIZE)

# Temps écoulé avant d'être considéré comme AFK
AFK_TIME = 120 # 120 secondes (2 minutes)

# ----------------------------- DÉFINITION DES BOUTONS -----------------------------
# Dictionaire des boutons du jeu
# Format type : {"nom button":{
#                       "x":position x,"y":position y,"button_size_widht":taille button,"button_size_height":hauteur button
#                       "color":couleur,"text": texte dans le button,"file":fichier pour l'image}}
buttons = {
    "launch":{
        "x":6,"y":9,
        "color":(255,255,255),"text":"Lancer le jeu","file":"assets/button.png"},

    "menu_settings":{
        "x":6,"y":14,
        "color":(255,255,255),"text":"Paramètres","file":"assets/button.png"},

    "game_settings":{
        "x":47,"y":33,
        "color":(255,255,255),"text":"","file":"assets\hud\settings.png"},

    "quit":{
        "x":15,"y":25,
        "color":(255,255,255),"text":"Quitter le jeu","file":"assets/button.png"},

    "return":{
        "x":6,"y":30,
        "color":(255,255,255),"text":"Retour","file":"assets/button.png"},
    
    "game_return":{
        "x":20,"y":8,
        "color":(255,255,255),"text":"Retour au jeu","file":"assets/button.png"},
    
    "menu_settings_return":{
        "x":20,"y":23,
        "color":(255,255,255),"text":"Retour au menu","file":"assets/button.png"},
    
    "save_and_quit":{
        "x":20,"y":23,
        "color":(255,255,255),"text":"Sauvegarder et quitter","file":"assets/button.png"},

    "credits":{
        "x":6,"y":19,
        "color":(255,255,255),"text":"Crédits","file":"assets/button.png"},
    "git":{
        "x":20,"y":18,
        "color":(255,255,255),"text":"Git","file":"assets/button.png"},
    "sound":{
        "x":20,"y":13,
        "color":(255,255,255),"text":"Son","file":"assets/button.png"},

    "seed":{
        "x":20,"y":18,
        "color":(255,255,255),"text":"Seed","file":"assets/button.png"},

    "return_menu":{
        "x":20,"y":18,
        "color":(255,255,255),"text":"Retour au menu","file":"assets/button.png"},

    "resolution_return":{
        "x":20,"y":29,
        "color":(255,255,255),"text":"Retour","file":"assets/button.png"},
    
    "resolution_game_return":{
        "x":20,"y":29,
        "color":(255,255,255),"text":"Retour","file":"assets/button.png"},

    "resolution_menu_screen":{
        "x":20,"y":8,
        "color":(255,255,255),"text":"Résolution","file":"assets/button.png"},

    "resolution_game_screen":{
        "x":31,"y":13,
        "color":(255,255,255),"text":"Résolution","file":"assets/button.png"},

    "full_screen":{
        "x":20,"y":4,
        "color":(255,255,255),"text":"Plein écran","file":"assets/button.png"},

    "resolution_1280x720":{
        "x":20,"y":9,
        "color":(255,255,255),"text":"1280x720","file":"assets/button.png"},

    "resolution_1920x1080":{
        "x":20,"y":19,
        "color":(255,255,255),"text":"1920x1080","file":"assets/button.png"},

    "resolution_1920x1200":{
        "x":20,"y":14,
        "color":(255,255,255),"text":"1920x1200","file":"assets/button.png"},

    "resolution_2560x1080":{
        "x":20,"y":24,
        "color":(255,255,255),"text":"2560x1080","file":"assets/button.png"},


    "respawn":{
        "x":24,"y":22,
        "color":(255,255,255),"text":"Respawn","file":"assets/button.png"},

    "default_planet":{
        "x":24,"y":22,
        "color":(255,255,255),"text":"Respawn","file":"assets/planet/default.png"},

    # Bouton pour tester l'upgrade de module de tier dans l'arbre technologique
    "test_upgrade_tech_tree_module":{
        "x":20,"y":30,
        "color":(255,255,255),"text":"Bouton test pour upgrade tier module tech tree","file":"assets/button.png"},

    "test_add_item":{
        "x":30,"y":20,
        "color":(255,255,255),"text":"Bouton test pour ajouter un item","file":"assets/button.png"},

    "test_remove_item":{
        "x":30,"y":25,
        "color":(255,255,255),"text":"Bouton test pour retirer un item","file":"assets/button.png"},

    "debug_add_item":{
        "x":50,"y":10,
        "color":(255,255,255),"text":"Bouton pour ajouter des items","file":"assets/button.png"},


    "tech_tree":{
        "x":11,"y":33,
        "color":(255,255,255),"text":"","file":'assets\hud/tech_tree.png'},

    "inventory":{
        "x":11,"y":31,
        "color":(255,255,255),"text":"","file":'assets\hud/inventory.png'},


    # Boutons de l'arbre technologique de la branche "moteurs"

    "ship_engine_tier_0":{
        "x":40,"y":20,
        "color":(255,255,255),"text":"Moteur T0","file":"assets/button.png","text_size":10},

    "ship_engine_tier_1":{
        "x":40,"y":23,
        "color":(255,255,255),"text":"Moteur T1","file":"assets/button.png","text_size":10},

    "ship_engine_tier_2":{
        "x":40,"y":26,
        "color":(255,255,255),"text":"Moteur T2","file":"assets/button.png","text_size":10},

    "ship_engine_tier_3":{
        "x":40,"y":29,
        "color":(255,255,255),"text":"Moteur T3","file":"assets/button.png","text_size":10},

    "ship_engine_tier_4":{
        "x":40,"y":32,
        "color":(255,255,255),"text":"Moteur T4","file":"assets/button.png","text_size":10},
    
    #boutons de l'arbre technologique de la branche "terraformation"

    "terraforming_tier_0":{
        "x":40,"y":3,
        "color":(255,255,255),"text":"Terraformation T0","file":"assets/button.png","text_size":10},
    
    "terraforming_tier_1":{
        "x":40,"y":6,
        "color":(255,255,255),"text":"Terraformation T1","file":"assets/button.png","text_size":10},

    "terraforming_tier_2":{
        "x":40,"y":9,
        "color":(255,255,255),"text":"Terraformation T2","file":"assets/button.png","text_size":10},
    
    "terraforming_tier_3":{
        "x":40,"y":12,
        "color":(255,255,255),"text":"Terraformation T3","file":"assets/button.png","text_size":10},
    
    "terraforming_tier_4":{
        "x":40,"y":15,
        "color":(255,255,255),"text":"Terraformation T4","file":"assets/button.png","text_size":10},

    # Boutons de l'arbre technologique de la branche "science de l'anti-matière"

    "antimatter_science_tier_0":{
        "x":20,"y":3,
        "color":(255,255,255),"text":"Science anti-matière T0","file":"assets/button.png","text_size":10},
    
    "antimatter_science_tier_1":{
        "x":20,"y":6,
        "color":(255,255,255),"text":"Science anti-matière T1","file":"assets/button.png","text_size":10},
    
    "antimatter_science_tier_2":{
        "x":20,"y":9,
        "color":(255,255,255),"text":"Science anti-matière T2","file":"assets/button.png","text_size":10},
    
    "antimatter_science_tier_3":{
        "x":20,"y":12,
        "color":(255,255,255),"text":"Science anti-matière T3","file":"assets/button.png","text_size":10},
    
    "antimatter_science_tier_4":{
        "x":20,"y":15,
        "color":(255,255,255),"text":"Science anti-matière T4","file":"assets/button.png","text_size":10},

    # Boutons de l'arbre technologique de la branche "radar"

    "radar_tier_0":{
        "x":5,"y":3,
        "color":(255,255,255),"text":"Radar T0","file":"assets/button.png","text_size":10},
    
    "radar_tier_1":{
        "x":5,"y":6,
        "color":(255,255,255),"text":"Radar T1","file":"assets/button.png","text_size":10},
    
    "radar_tier_2":{
        "x":5,"y":9,
        "color":(255,255,255),"text":"Radar T2","file":"assets/button.png","text_size":10},
    
    # Boutons de l'arbre technologique de la branche "defenses"

    "defenses_T0":{
        "x":5,"y":25,
        "color":(255,255,255),"text":"Défenses T0","file":"assets/button.png","text_size":10},
    
    "defenses_T1":{
        "x":13,"y":25,
        "color":(255,255,255),"text":"Défenses T1","file":"assets/button.png","text_size":10},
    
    "defenses_T2":{
        "x":21,"y":25,
        "color":(255,255,255),"text":"Défenses T2","file":"assets/button.png","text_size":10},

    "button_test_click":{
        "x":40,"y":20,
        "color":(255,255,255),"text":"Bouton test click","file":"assets/button.png"},


    "mines_buy":{
        "x":13,"y":15,
        "color":(255,255,255),"text":"acheter","file":"assets/button.png"},
}