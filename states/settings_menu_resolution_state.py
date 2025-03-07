import pygame
from buttons.button import return_button,style_image,resolution_screen_button
from .base_state import BaseState




class MenuSettingsResolutionState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

    def handle_event(self, event,pos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            from .menu_state import MenuState
            self.state_manager.set_state(MenuState(self.state_manager))


    def update(self, dt, actions,pos):

        mouse_x,mouse_y=pos
        if return_button().click(mouse_x,mouse_y):
            from states.settings_menu_state import MenuSettingsState
            self.state_manager.set_state(MenuSettingsState(self.state_manager))     #changer le state


        if resolution_screen_button().click(mouse_x,mouse_y):
            pass


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))
        return_button().draw()

        pass
