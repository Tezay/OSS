import pygame
from buttons import*
from ..base_state import BaseState
from config import WINDOW_WIDTH,WINDOW_HEIGHT
from .settings_game_state import resolution

global MAX_WINDOW_HEIGHT, MAX_WINDOW_WIDTH

pygame.init()
info = pygame.display.Info()
MAX_WINDOW_WIDTH=info.current_w
MAX_WINDOW_HEIGHT=info.current_h


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class MenuSettingsResolutionState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

    def handle_event(self, event,pos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            from ..menu_state import MenuState
            # Passe l'état courant à menu_state
            self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):
        # Définition des variables de taille de l'écran (globales)
        global WINDOW_WIDTH, WINDOW_HEIGHT,button_size_widht,button_size_height

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if return_button().click(mouse_x,mouse_y):
                from .settings_menu_state import MenuSettingsState
                from .settings_game_state import GameSettingsState
                # Passe l'état courant à menu_settings_state
                if resolution!=1:
                    self.state_manager.set_state(MenuSettingsState(self.state_manager))
                else:
                    self.state_manager.set_state(GameSettingsState(self.state_manager,self.game))

                
            if full_screen_button().click(mouse_x,mouse_y):
                pygame.display.set_mode((MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT), pygame.FULLSCREEN)  # Activer le mode plein écran

            if resolution_1280x720_button().click(mouse_x,mouse_y):
                WINDOW_WIDTH = 1280
                WINDOW_HEIGHT = 720
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

            if resolution_1920x1200_button().click(mouse_x,mouse_y):
                WINDOW_WIDTH = 1920
                WINDOW_HEIGHT = 1200
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) 
            
            if resolution_1920x1080_button().click(mouse_x,mouse_y):
                WINDOW_WIDTH = 1920
                WINDOW_HEIGHT = 1080
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

            if resolution_2560x1080_button().click(mouse_x,mouse_y):
                WINDOW_WIDTH = 2560
                WINDOW_HEIGHT = 1080
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        # Dessin des boutons relatifs à l'état settings_menu_resolution_state (avec la méthode .draw() de la classe Button)
        return_button().draw()
        full_screen_button().draw()
        resolution_1280x720_button().draw()
        resolution_1920x1200_button().draw()
        resolution_1920x1080_button().draw()
        resolution_2560x1080_button().draw()
