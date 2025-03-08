from .base_state import BaseState
from buttons.button import *
from .game_state import GameState
from.settings_menu_state import MenuSettingsState
import main


class MenuState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        # Exemple d'éléments à afficher
        self.title_font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 32)

    def handle_event(self, event,pos):
        pass

    def update(self, dt, actions,pos):
        # Si l'action "start_game" (définie dans config.py) est True, on passe au GameState
        """if actions.get("start_game"):
            from .game_state import GameState
            self.state_manager.set_state(GameState(self.state_manager)"""

        mouse_x,mouse_y=pos

        if launch_button().click(mouse_x,mouse_y):     #verifie si il y a un clique sur le bouton de lounch
            self.state_manager.set_state(GameState(self.state_manager))     #changer le state

        if menu_settings_button().click(mouse_x,mouse_y):      #verifie si il y a un clique sur le bouton de parametre
            setting_quit = 2
            self.state_manager.set_state(MenuSettingsState(self.state_manager))     #changer le state

        if quit_button().click(mouse_x,mouse_y):       #verifie si il y a un clique sur le bouton de quiter le jeu
            #permet de quitter le programe dans le main via le bouton
            pygame.event.post(pygame.event.Event(pygame.QUIT))




    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        """title_surf = self.title_font.render("Menu Principal", True, (255, 255, 255))
        info_surf = self.info_font.render("Appuyez sur ENTER pour lancer le jeu", True, (200, 200, 200))"""


        """if menu_settings_button().normal_picture("rect").collidepoint(pygame.mouse.get_pos()):
            screen.blit(menu_settings_button().hoover_picture("picture"), menu_settings_button().hoover_picture("rect"))
        else:
            screen.blit(menu_settings_button().normal_picture("picture"), menu_settings_button().normal_picture("rect"))"""

        launch_button().draw()    #demander a cousseau si besois d'aide wallah je suis programmeur pas prof de français
        menu_settings_button().draw()
        quit_button().draw()      #pareil wallah


        """screen.blit(title_surf, (100, 100))
        screen.blit(info_surf, (100, 200))"""
