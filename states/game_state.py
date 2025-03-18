import pygame
import math
import random
from config import KEY_BINDINGS, SPACESHIP_ROTATION_SPEED, SPACESHIP_MASS
from .base_state import BaseState
from buttons import *
from game import Game
from map_generator import generate_map
from spaceship import Spaceship
from camera import Camera
import config


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class GameState(BaseState):
    def __init__(self, state_manager, existing_game=None):
        super().__init__()
        self.state_manager = state_manager

        # Vérification si un état game déjà crée a été transmis en paramètre
        # Note : Permet d'éviter de regénérer entièrement la map lors de changement d'état
        if existing_game is not None:
            # Réutilisation de l'existant (même map, même vaisseau, etc.)
            self.game = existing_game
            
        # Sinon création d'un nouveau Game + nouvelle map + nouveau vaisseau
        else:
            # Création de la classe Game
            self.game = Game()

            # Selection de la seed
            if config.custom_seed is None:
                if DEFAULT_SEED is None:
                    seed = random.randint(0, 999999999)
                else:
                    seed = DEFAULT_SEED
            else:
                seed = config.custom_seed
            print(f"Seed: {seed}")

            # Génération de la map
            background_stars, planets = generate_map(seed, WORLD_WIDTH, WORLD_HEIGHT, NUMBER_OF_PLANETS)
            print("Map generated.")

            # Injecter les étoiles et planètes dans Game
            self.game.set_background_stars(background_stars)
            self.game.set_planets(planets)

            # Création du vaisseau
            spaceship = Spaceship(
                x=WORLD_WIDTH//2,
                y=WORLD_HEIGHT//2,
                vx=0, vy=-10, # Vitesse par défaut de 10 pixel vers le haut
                width=20, height=20,
                image_path=SPACESHIP_TEXTURE_DEFAULT_PATH,
                mass=SPACESHIP_MASS
            )
            self.game.set_spaceship(spaceship)

            # Création de la caméra
            camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
            if not DEBUG_MODE:
                camera.set_target(spaceship)
            self.game.set_camera(camera)

    def handle_event(self, event, pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:

            # Vérification de la touche associée au menu inventaire (si préssée, change l'état courant à inventory_state)
            if event.key == KEY_BINDINGS["inventory"]:
                from .inventory_state import InventoryState
                self.state_manager.set_state(InventoryState(self.state_manager, self.game))

            # Ajout du passage à l'état Game Over avec "G"
            if event.key == KEY_BINDINGS["game_over"]:
                print("Game Over lancé !")
                from .game_over_state import GameOverState
                self.state_manager.set_state(GameOverState(self.state_manager, self.game))

            # Décélération instantanée (test, ne pas garder pour version finale)
            if event.key == KEY_BINDINGS["spaceship_deceleration"]:
                vx, vy = self.game.spaceship.vx, self.game.spaceship.vy
                speed = math.sqrt(vx**2 + vy**2)
                if speed > 1e-3:
                    decel_force = 3000
                    nx, ny = vx / speed, vy / speed
                    fx = -decel_force * nx
                    fy = -decel_force * ny
                    self.game.spaceship.add_force(fx, fy)

            # Arrêt instantané (mode debug)
            if DEBUG_MODE and event.key == KEY_BINDINGS["spaceship_stop"]:
                self.game.spaceship.vx = 0
                self.game.spaceship.vy = 0

    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos
        
        if mouse_clicked:
            # Vérification du clique de la souris sur le bouton
            if click_button('game_settings',pos):
                from .settings_state.settings_game_state import GameSettingsState
                # Passe l'état courant à game_settings_state
                self.state_manager.set_state(GameSettingsState(self.state_manager,self.game))  # changer le state

            # Vérification du clique de la souris sur le bouton
            if click_button("tech_tree",pos):
                from .tech_tree_state import TechTreeState
                # Définie l'état courant à TechTreeState
                # Note : self.game passé en paramètre, pour pouvoir récupérer la game en court (ne pas regénérer la map)
                self.state_manager.set_state(TechTreeState(self.state_manager,self.game))

        # Rotation gauche
        if actions["spaceship_rotate_left"]:
            # Rotation à gauche : applique angle négatif
            # SPACESHIP_ROTATION_SPEED est en deg/s => multiplier par dt
            self.game.spaceship.rotate(-SPACESHIP_ROTATION_SPEED * dt)
            self.game.spaceship.update_image_angle()

        # Rotation droite
        if actions["spaceship_rotate_right"]:
            self.game.spaceship.rotate(SPACESHIP_ROTATION_SPEED * dt)
            self.game.spaceship.update_image_angle()

        # Poussée continue si touche préssée
        if actions["spaceship_move"]:

            # Conversion de l’angle en radians
            rad = math.radians(self.game.spaceship.angle)

            # Application de la force en direction du vaisseau
            fx = SPACESHIP_THRUST_FORCE * math.sin(rad)
            fy = -SPACESHIP_THRUST_FORCE * math.cos(rad)

            # Si le vaisseau est dans l'état atterri, lui permettre de redécoller
            if self.game.spaceship.is_landed:
                # Le booléen repasse à False 
                self.game.spaceship.is_landed = False
                # Application d'une force de poussé supplémentaire, pour facilité le décrochement du vaisseau de l'attraction gravitationnelle de la planète
                planet_mass = self.game.spaceship.landed_planet.mass
                # Arbitrairement, j'ai trouvé que la masse de la planète / 1e5*G fonctionnait bien
                takeoff_force_coeff = planet_mass/1e5*G
                self.game.spaceship.add_force(fx*takeoff_force_coeff, fy*takeoff_force_coeff)

            # Application de la force au vaisseau
            self.game.spaceship.add_force(fx, fy)

        # Update de GameState
        self.game.update(dt, actions)
        
    def draw(self, screen, pos):

        # Dessin du jeu (espace 2d avec planètes et vaisseau, HUD, minimap etc.)
        self.game.draw(screen)