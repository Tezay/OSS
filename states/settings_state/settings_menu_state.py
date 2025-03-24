import pygame

from gui.buttons import *
from ..base_state import BaseState


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class MenuSettingsState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager      

    def handle_event(self, event,pos):
        if event.type == pygame.KEYDOWN:

            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from ..menu_state import MenuState
                self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):
        
        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("return",pos):
                from states.menu_state import MenuState
                # Passe l'état courant à menu_state
                self.state_manager.set_state(MenuState(self.state_manager))

            # Vérification du clique de la souris sur le boutons
            if click_button("resolution_menu_screen",pos):
                from .settings_menu_resolution_state import MenuSettingsResolutionState
                # Passe l'état courant à menu_settings_resulutions_state
                self.state_manager.set_state(MenuSettingsResolutionState(self.state_manager))
            
            if click_button("seed",pos):
                from .settings_menu_seed_state import MenuSettingsSeedState
                # Passe l'état courant à menu_settings_seed_state
                self.state_manager.set_state(MenuSettingsSeedState(self.state_manager))


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        # Dessin des boutons relatifs à l'état settings_menu_state (avec la méthode .draw() de la classe Button)
        draw_buttons("return")
        draw_buttons("resolution_menu_screen")
        draw_buttons("seed")


