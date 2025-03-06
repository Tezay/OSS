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
        pass

    def update(self, dt, actions,pos):

        mouse_x,mouse_y=pos
        variable=1
        """if close().click(mouse_x,mouse_y):
            from states.game_state import GameState
            from states.menu_state import MenuState
            from states.game_state import settings_quit
            from states.menu_state import settings_quit

            if settings_quit==1:
                self.state_manager.set_state(GameState(self.state_manager))     #changer le state
            elif settings_quit==2:
                self.state_manager.set_state(MenuState(self.state_manager))
        pass"""

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))
        close().draw()

        pass
