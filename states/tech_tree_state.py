import pygame
from buttons import*
from .base_state import BaseState


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class TechTreeState(BaseState):
    def __init__(self, state_manager,game):
        super().__init__()
        self.state_manager = state_manager
        self.game=game

    def handle_event(self, event,pos):
        pass

    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if return_button().click(mouse_x,mouse_y):
                from states.game_state import GameState
                new_game_state = GameState(self.state_manager)
                # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
                new_game_state.game = self.game
                # Passe l'état courant à game_state
                self.state_manager.set_state(new_game_state)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                from .game_state import GameState
                new_game_state = GameState(self.state_manager)
                # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
                new_game_state.game = self.game
                # Changer l'état courant à game_state
                self.state_manager.set_state(new_game_state)

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))
        return_button().draw()

        # Dessin des boutons relatifs à l'état tech_tree_state (avec la méthode .draw() de la classe Button)
        # Bouton test
        test().draw()
