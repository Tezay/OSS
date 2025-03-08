import pygame
from buttons.button import*
from ..base_state import BaseState
from config import WINDOW_WIDTH,WINDOW_HEIGHT

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
            self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions,pos):
        global WINDOW_WIDTH, WINDOW_HEIGHT,button_size_widht,button_size_height   # définir les variables comme globales
        mouse_x,mouse_y=pos
        if return_button().click(mouse_x,mouse_y):
            from .settings_menu_state import MenuSettingsState
            self.state_manager.set_state(MenuSettingsState(self.state_manager))     #changer le state

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

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        # Dessin des boutons relatifs à l'état settings_menu_resolution_state (avec la méthode .draw() de la classe Button)
        return_button().draw()
        full_screen_button().draw()
        resolution_1280x720_button().draw()
        resolution_1920x1200_button().draw()
        resolution_1920x1080_button().draw()
