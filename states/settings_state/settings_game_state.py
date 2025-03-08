import pygame
from buttons.button import*
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
        pass


    def update(self, dt, actions,pos):

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos
        # Vérification du clique de la souris sur le bouton
        if return_button().click(mouse_x,mouse_y):
            from states.game_state import GameState
            new_game_state = GameState(self.state_manager)
            # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
            new_game_state.game = self.game
            # Changer l'état courant à game_state
            self.state_manager.set_state(new_game_state)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            from ..game_state import GameState
            new_game_state = GameState(self.state_manager)
            # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
            new_game_state.game = self.game
            # Changer l'état courant à game_state
            self.state_manager.set_state(new_game_state)

        # Vérifie s'il y a un clique sur le bouton pour quitter
        if quit_button().click(mouse_x,mouse_y):
            # Quitte le programme depuis le main
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        # Dessin des boutons relatifs à l'état setting_game_state (avec la méthode .draw() de la classe Button)
        return_button().draw()
        quit_button().draw()
