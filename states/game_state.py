import pygame
import math
import random
from config import KEY_BINDINGS, SPACESHIP_ROTATION_SPEED
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
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        # Création de Game (ne génère rien)
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
        planets = generate_map(seed, WORLD_WIDTH, WORLD_HEIGHT, NUMBER_OF_PLANETS)
        print("Map generated.")

        # Injecter ces planètes dans Game
        self.game.set_planets(planets)

        # Création du vaisseau
        spaceship = Spaceship(
            x=WORLD_WIDTH//2,
            y=WORLD_HEIGHT//2,
            vx=0, vy=0,
            width=20, height=20,
            image_path=SPACESHIP_TEXTURE_DEFAULT_PATH,
            mass=10
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

            # Vérification de la touche associée au menu pause (si préssée, change l'état courant à pause_state)
            if event.key == KEY_BINDINGS["pause"]:
                from .pause_state import PauseState
                self.state_manager.set_state(PauseState(self.state_manager, self.game))

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
            self.game.spaceship.add_force(fx, fy)

        # Update de GameState
        self.game.update(dt, actions)
        
    def draw(self, screen, pos):

        # Dessin du jeu (espace 2d avec planètes et vaisseau, HUD, minimap etc.)
        self.game.draw(screen)