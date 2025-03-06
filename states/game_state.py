import pygame
from .base_state import BaseState
from game import Game
from config import KEY_BINDINGS
from buttons.button import *
from.settings_game_state import GameSettingsState



class GameState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.game=Game()

    def handle_event(self, event,pos):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["pause"]:
                from .pause_state import PauseState
                setting_quit=1
                self.state_manager.set_state(PauseState(self.state_manager, self.game))

    def update(self, dt, actions,pos):
        mouse_x, mouse_y=pos
        if game_settings().click(mouse_x, mouse_y):  # verifie si il y a un clique sur le bouton de parametre
            self.state_manager.set_state(GameSettingsState(self.state_manager,self.game))  # changer le state
        self.game.update(dt, actions)

        if tech_tree().click(mouse_x,mouse_y):
            from .tech_tree_state import TechTreeState
            self.state_manager.set_state(TechTreeState(self.state_manager,self.game))  # changer le state
        self.game.update(dt, actions)


    def draw(self, screen,pos):
        self.game.draw(screen)

        style_image(game_settings)
        style_image(tech_tree)
