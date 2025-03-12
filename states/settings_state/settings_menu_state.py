import pygame
from buttons import return_button,resolution_screen_button,seed_button
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            from ..menu_state import MenuState
            self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):
        
        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if return_button().click(mouse_x,mouse_y):
                from states.menu_state import MenuState
                # Passe l'état courant à menu_state
                self.state_manager.set_state(MenuState(self.state_manager))

            # Vérification du clique de la souris sur le boutons
            if resolution_screen_button().click(mouse_x,mouse_y):
                from .settings_menu_resolution_state import MenuSettingsResolutionState
                # Passe l'état courant à menu_settings_resulutions_state
                self.state_manager.set_state(MenuSettingsResolutionState(self.state_manager))
            
            if seed_button().click(mouse_x,mouse_y):
                from .settings_menu_seed_state import MenuSettingsSeedState
                # Passe l'état courant à menu_settings_seed_state
                self.state_manager.set_state(MenuSettingsSeedState(self.state_manager))


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        # Dessin des boutons relatifs à l'état settings_menu_state (avec la méthode .draw() de la classe Button)
        return_button().draw()
        resolution_screen_button().draw()
        seed_button().draw()
