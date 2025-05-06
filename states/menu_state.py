from .base_state import BaseState
from gui.buttons import *
from .game_state import GameState
from .settings_state.settings_menu_state import MenuSettingsState
from .credits_state import CreditsState

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
        self.size=custom_size(16,4)

    def handle_event(self, event,pos):

        if event.type == pygame.KEYDOWN:
            # Vérification de la touche associée au démarrage du jeu
            if event.key == KEY_BINDINGS["start_game"]:
                from .game_state import GameState
                # Réinitialiser le timer persistant avant de lancer une nouvelle partie
                self.state_manager.reset_persistent_timer()
                # Passe l'état courant à game_state
                self.state_manager.set_state(GameState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("launch",pos,self.size): 
                # Réinitialiser le timer persistant avant de lancer une nouvelle partie
                self.state_manager.reset_persistent_timer()
                # Passe l'état courant à game_state
                self.state_manager.set_state(GameState(self.state_manager))

            # Vérification du clique de la souris sur le bouton
            if click_button("menu_settings",pos,self.size):
                print("clique")
                # Passe l'état courant à menu_settings_state
                self.state_manager.set_state(MenuSettingsState(self.state_manager))

            # Vérification du clique de la souris sur le bouton
            if click_button("quit",pos,self.size):
                #permet de quitter le programe dans le main via le bouton
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            # Vérification du clique de la souris sur le bouton Credits
            if click_button("credits",pos,self.size):
                self.state_manager.set_state(CreditsState(self.state_manager))

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        if DEBUG_MODE:
            # Affiche la grille si on passe en paramètre True
            grille(True)

        # Dessin des boutons relatifs à l'état menu_state (avec la méthode .draw() de la classe Button)

        draw_size_buttons("launch",6,9,custom_size(16,4))
        draw_size_buttons("menu_settings",6,14,custom_size(16,4))
        draw_size_buttons("quit",6,24,custom_size(16,4))
        draw_size_buttons("credits",6,19,custom_size(16,4))

