from .base_state import BaseState
from buttons import *


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class PauseState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = pygame.font.Font(None, 50)

    def handle_event(self, event,pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["pause"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

    def update(self, dt, actions, pos, mouse_clicked):
        # Pas besoin de surveiller actions["pause"] ici
        pass

    def draw(self, screen,pos):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        text_surf = self.font.render("Jeu en pause - appuyez sur P pour reprendre", True, (255, 255, 255))
        rect = text_surf.get_rect(center=screen.get_rect().center)
        screen.blit(text_surf, rect)
