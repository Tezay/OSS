import pygame
from buttons import*
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            from ..game_state import GameState
            new_game_state = GameState(self.state_manager)
            # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
            new_game_state.game = self.game
            # Changer l'état courant à game_state
            self.state_manager.set_state(new_game_state)


    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("return_menu",pos):
                from states.menu_state import MenuState
                new_game_state = MenuState(self.state_manager)
                new_game_state.game = self.game
                # Changer l'état courant à game_state
                self.state_manager.set_state(new_game_state)             

            if click_button("return",pos):
                from states.game_state import GameState
                new_game_state = GameState(self.state_manager)
                # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
                new_game_state.game = self.game
                # Changer l'état courant à game_state
                self.state_manager.set_state(new_game_state)

            if click_button("resolution_game_screen",pos):
                from .settings_game_resolution_state import GameSettingsResolutionState
                new_game_state = GameSettingsResolutionState(self.state_manager)
                # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
                new_game_state.game = self.game
                # Changer l'état courant à game_state
                self.state_manager.set_state(new_game_state)


        # Vérifie s'il y a un clique sur le bouton pour quitter
        if click_button("quit",pos):
            # Quitte le programme depuis le main
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        # Dessin des boutons relatifs à l'état setting_game_state (avec la méthode .draw() de la classe Button)
        draw_buttons("resolution_game_screen")
        draw_buttons("return")
        draw_buttons("quit")
        draw_buttons("return_menu")


