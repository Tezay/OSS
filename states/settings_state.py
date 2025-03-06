import pygame
from buttons.button import close



class SettingsState():
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

    def handle_event(self, event,pos):
        if event==pygame.K_ESCAPE:
            from .game_state import GameState
            print("ca marche pas")
            self.state_manager.set_state(GameState(self.state_manager))


    def update(self, dt, actions,pos):

        mouse_x,mouse_y=pos
        if close().click(mouse_x,mouse_y):
            from states.menu_state import MenuState
            self.state_manager.set_state(MenuState(self.state_manager))     #changer le state)


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))
        close().draw()

        pass
