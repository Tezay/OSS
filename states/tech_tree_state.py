import pygame
from buttons.button import*
from .base_state import BaseState



class TechTreeState(BaseState):
    def __init__(self, state_manager,game):
        super().__init__()
        self.state_manager = state_manager
        self.game=game

    def handle_event(self, event,pos):
        if event==pygame.K_ESCAPE:
            from .game_state import GameState
            self.state_manager.set_state(GameState(self.state_manager))


    def update(self, dt, actions,pos):

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos
        if return_button().click(mouse_x,mouse_y):
            from states.game_state import GameState
            new_game_state = GameState(self.state_manager)
            # Réinitialisation de l'objet self.game pour ne pas réinitialiser la map
            new_game_state.game = self.game
            self.state_manager.set_state(new_game_state)     #changer le state)


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))
        return_button().draw()

        style_image(test)

        pass
