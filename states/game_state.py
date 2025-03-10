import pygame
from .base_state import BaseState
from game import Game
from config import KEY_BINDINGS, SPACESHIP_DEFAULT_ACCELERATION
from buttons import *
from spaceship import Spaceship


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class GameState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.game=Game()

    def handle_event(self, event,pos):
        if event.type == pygame.KEYDOWN:
            # Vérification de la touche associée au menu pause (si préssée, change le state à pause_state)
            if event.key == KEY_BINDINGS["pause"]:
                from .pause_state import PauseState
                setting_quit=1 # wtf ?
                self.state_manager.set_state(PauseState(self.state_manager, self.game))

            ##################### TEST #######################
            # Vérification de la touche associée au déplacement du vaisseau
            if event.key == KEY_BINDINGS["spaceship_move"]:
                # Test de déplacement vers le haut (on applique une accélération au vaisseau)
                self.game.spaceship.accelerate(0, -SPACESHIP_DEFAULT_ACCELERATION)
            
            if event.key == KEY_BINDINGS["spaceship_deceleration"]:
                # Test décélération du vaisseau (appliquer accélération inverse)
                self.game.spaceship.accelerate(0, SPACESHIP_DEFAULT_ACCELERATION)

            if event.key == KEY_BINDINGS["spaceship_stop"]:
                # Test pour arrêter le déplacement du vaisseau instantanément
                self.game.spaceship.vx = 0
                self.game.spaceship.vy = 0
            #################################################

            

    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if game_settings_button().click(mouse_x, mouse_y):
            from .settings_state.settings_game_state import GameSettingsState
            # Passe l'état courant à game_settings_state
            self.state_manager.set_state(GameSettingsState(self.state_manager,self.game))  # changer le state
        
        # Vérification du clique de la souris sur le bouton
        if tech_tree_button().click(mouse_x,mouse_y):
            from .tech_tree_state import TechTreeState
            # Définie l'état courant à TechTreeState
            # Note : self.game passé en paramètre, pour pouvoir récupérer la game en court (ne pas regénérer la map)
            self.state_manager.set_state(TechTreeState(self.state_manager,self.game))

        # Update de GameState
        self.game.update(dt, actions)
        
    def draw(self, screen,pos):

        # Dessin du jeu (espace 2d avec planètes et vaisseau)
        self.game.draw(screen)

        # Dessin des boutons relatifs à l'état game_state (avec la méthode .draw() de la classe Button)
        game_settings_button().draw()
        tech_tree_button().draw()