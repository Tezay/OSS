import pygame
from .base_state import BaseState
from game import Game
from config import KEY_BINDINGS
from buttons.button import *
from.settings_state import SettingsState



class GameState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.game = Game()

    def handle_event(self, event,pos):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["pause"]:
                from .pause_state_game import PauseState
                setting_quit=1
                self.state_manager.set_state(PauseState(self.state_manager, self.game))

    def update(self, dt, actions,pos):
        mouse_x, mouse_y=pos
        if settings(1).click(mouse_x, mouse_y):  # verifie si il y a un clique sur le bouton de parametre
            self.state_manager.set_state(SettingsState(self.state_manager))  # changer le state
        self.game.update(dt, actions)

    def draw(self, screen,pos):
        self.game.draw(screen)

        if settings(1).normal_picture("rect").collidepoint(pygame.mouse.get_pos()):
            screen.blit(settings(1).hoover_picture("picture"), settings(1).hoover_picture("rect"))
        else:
            screen.blit(settings(1).normal_picture("picture"), settings(1).normal_picture("rect"))
