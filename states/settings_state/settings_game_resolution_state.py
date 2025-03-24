import pygame

from gui.buttons import *
from ..base_state import BaseState
from config import WINDOW_WIDTH,WINDOW_HEIGHT
from core.game import Game



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
class GameSettingsResolutionState(BaseState):
    def __init__(self, state_manager,game):
        super().__init__()
        self.state_manager = state_manager
        self.game=game


    def handle_event(self, event,pos):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from .settings_game_state import GameSettingsState
                # Passe l'état courant à setting_game_state
                self.state_manager.set_state(GameSettingsState(self.state_manager,self.game))

    def update(self, dt, actions, pos, mouse_clicked):
        # Définition des variables de taille de l'écran (globales)
        global WINDOW_WIDTH, WINDOW_HEIGHT,button_size_widht,button_size_height

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("resolution_game_return",pos,custom_size(20,4)):
                from .settings_game_state import GameSettingsState
                # Passe l'état courant à game_settings_state
                self.state_manager.set_state(GameSettingsState(self.state_manager,self.game))
                
            if click_button("full_screen",pos,custom_size(20,4)):
                pygame.display.set_mode((MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)  # Activer le mode plein écran

            if click_button("resolution_1280x720",pos,custom_size(20,4)):
                WINDOW_WIDTH = 1280
                WINDOW_HEIGHT = 720
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

            if click_button("resolution_1920x1200",pos,custom_size(20,4)):
                WINDOW_WIDTH = 1920
                WINDOW_HEIGHT = 1200
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) 
            
            if click_button("resolution_1920x1080",pos,custom_size(20,4)):
                WINDOW_WIDTH = 1920
                WINDOW_HEIGHT = 1080
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

            if click_button("resolution_2560x1080",pos,custom_size(20,4)):
                WINDOW_WIDTH = 2560
                WINDOW_HEIGHT = 1080
                pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    def draw(self, screen,pos):
        
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Dessin des boutons relatifs à l'état settings_menu_resolution_state (avec la méthode .draw() de la classe Button)

        draw_size_buttons("full_screen",20,4,custom_size(20,4))
        draw_size_buttons("resolution_1280x720",20,9,custom_size(20,4))
        draw_size_buttons("resolution_1920x1200",20,14,custom_size(20,4))
        draw_size_buttons("resolution_1920x1080",20,19,custom_size(20,4))
        draw_size_buttons("resolution_2560x1080",20,24,custom_size(20,4))
        draw_size_buttons("resolution_game_return",20,29,custom_size(20,4))
