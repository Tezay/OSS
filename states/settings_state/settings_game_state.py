import pygame

from gui.buttons import *
from ..base_state import BaseState


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class GameSettingsState(BaseState):
    def __init__(self, state_manager,game):
        super().__init__()
        self.state_manager = state_manager
        self.game=game

    def handle_event(self, event,pos):
        if event.type == pygame.KEYDOWN:

            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from ..game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)


    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("return_menu",pos,custom_size(30,4)):
                from states.menu_state import MenuState
                new_game_state = MenuState(self.state_manager)
                new_game_state.game = self.game
                # Changer l'état courant à game_state
                self.state_manager.set_state(new_game_state)             

            if click_button("game_return",pos,custom_size(30,4)):
                from states.game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

            if click_button("resolution_game_screen",pos,custom_size(14,4)):
                from .settings_game_resolution_state import GameSettingsResolutionState
                new_game_state = GameSettingsResolutionState(self.state_manager,self.game)
                # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
                new_game_state.game = self.game
                # Changer l'état courant à game_state
                self.state_manager.set_state(new_game_state)
            
            if click_button("debug_add_item",pos):
                self.game.data_manager.inventory.debug_add_item("test_item")


        # Vérifie s'il y a un clique sur le bouton pour quitter
        if click_button("save_and_quit",pos,custom_size(30,4)):
            # Quitte le programme depuis le main
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        


    def draw(self, screen,pos):
        
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Dessin des boutons relatifs à l'état setting_game_state (avec la méthode .draw() de la classe Button)

        draw_size_buttons("game_return",20,8,custom_size(20,4))
        draw_size_buttons("resolution_game_screen",30.5,13,custom_size(9.5,4))
        draw_size_buttons("sound",20,13,custom_size(9.5,4))
        draw_size_buttons("return_menu",20,18,custom_size(20,4))
        draw_size_buttons("save_and_quit",20,23,custom_size(20,4))



