from .base_state import BaseState
from buttons.button import *
from .game_state import GameState
from .settings_state.settings_menu_state import MenuSettingsState

# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
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

        # Récupération des coordonnées de la souris
        mouse_x,mouse_y=pos
        # Vérification du clique de la souris sur le bouton
        if launch_button().click(mouse_x,mouse_y):
            # Passe l'état courant à game_state
            self.state_manager.set_state(GameState(self.state_manager))

        # Vérification du clique de la souris sur le bouton
        if menu_settings_button().click(mouse_x,mouse_y):
            setting_quit = 2
            # Passe l'état courant à menu_settings_state
            self.state_manager.set_state(MenuSettingsState(self.state_manager))

        # Vérification du clique de la souris sur le bouton
        if quit_button().click(mouse_x,mouse_y):
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

        # Dessin des boutons relatifs à l'état menu_state (avec la méthode .draw() de la classe Button)
        launch_button().draw()
        menu_settings_button().draw()
        quit_button().draw()

        """screen.blit(title_surf, (100, 100))
        screen.blit(info_surf, (100, 200))"""
