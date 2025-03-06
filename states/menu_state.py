from .base_state import BaseState
from buttons.button import *
from .game_state import GameState
from.settings_state import SettingsState




class MenuState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        # Exemple d'éléments à afficher
        self.title_font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        # On peut gérer des événements de souris / clavier ici si besoin
        pass

    def update(self, dt, actions,pos):
        # Si l'action "start_game" (définie dans config.py) est True, on passe au GameState
        """if actions.get("start_game"):
            from .game_state import GameState
            self.state_manager.set_state(GameState(self.state_manager)"""

        mouse_x,mouse_y=pos

        if lounch().click(mouse_x,mouse_y):     #verifie si il y a un clique sur le bouton de lounch
            self.state_manager.set_state(GameState(self.state_manager))     #changer le state

        if settings(1).click(mouse_x,mouse_y):     #verifie si il y a un clique sur le bouton de parametre
            self.state_manager.set_state(SettingsState(self.state_manager))     #changer le state


    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        """title_surf = self.title_font.render("Menu Principal", True, (255, 255, 255))
        info_surf = self.info_font.render("Appuyez sur ENTER pour lancer le jeu", True, (200, 200, 200))"""


        if settings(0).normal_picture("rect").collidepoint(pygame.mouse.get_pos()):
            screen.blit(settings(0).hoover_picture("picture"), settings(0).hoover_picture("rect"))
        else:
            screen.blit(settings(0).normal_picture("picture"), settings(0).normal_picture("rect"))

        if lounch().normal_picture("rect").collidepoint(pygame.mouse.get_pos()):
            screen.blit(lounch().hoover_picture("picture"), lounch().hoover_picture("rect"))
        else:
            screen.blit(lounch().normal_picture("picture"), lounch().normal_picture("rect"))

        """screen.blit(title_surf, (100, 100))
        screen.blit(info_surf, (100, 200))"""
