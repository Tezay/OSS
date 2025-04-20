import pygame
from pygame import Rect

from gui.buttons import *
from .base_state import BaseState


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class CreditsState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

    def handle_event(self, event, pos):
        if event.type == pygame.KEYDOWN:

            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from states.menu_state import MenuState
                self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("menu_settings_return", pos, custom_size(30, 4)):
                from states.menu_state import MenuState
                # Passe l'état courant à menu_state
                self.state_manager.set_state(MenuState(self.state_manager))
            if click_button("git",pos,custom_size(30,4)):
                print("git")
                import webbrowser
                webbrowser.open('https://github.com/Tezay/OSS.git')

    def draw(self, screen, pos):
        screen.fill((0, 0, 0))
        zone = Rect(200,200,100,50)
        x,y=zone.topleft
        x,y=screen.blit(custom_font.render("CUPILLARD Eliot", True, (255,255,255)), (x,y)).bottomleft
        x,y=screen.blit(custom_font.render("TORRES Edouard", True, (255,255,255)), (x,y)).bottomleft
        x,y=screen.blit(custom_font.render("COUSSEAU Eliot", True, (255,255,255)), (x,y)).bottomleft
        x, y = screen.blit(custom_font.render("DEHEZ Delphine", True, (255, 255, 255)), (x, y)).bottomleft
        x, y = screen.blit(custom_font.render("FOURNIER Aurélia", True, (255, 255, 255)), (x, y)).bottomleft
        #screen.update(zone)
        # Dessin des boutons relatifs à l'état settings_menu_state (avec la méthode .draw() de la classe Button)
        draw_size_buttons("git",20,18,custom_size(20,4))
        draw_size_buttons("menu_settings_return", 20, 23, custom_size(20, 4))




