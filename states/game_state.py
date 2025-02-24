import pygame
from .base_state import BaseState
from game import Game
from config import KEY_BINDINGS

class GameState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.game = Game()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["pause"]:
                from .pause_state import PauseState
                self.state_manager.set_state(PauseState(self.state_manager, self.game))

    def update(self, dt, actions):
        # Le reste de la logique (caméra, etc.) s'appuie sur actions
        self.game.update(dt, actions)

    def draw(self, screen):
        self.game.draw(screen)
