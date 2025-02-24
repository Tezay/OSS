import pygame
from .base_state import BaseState

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

    def update(self, dt, actions):
        # Si l'action "start_game" (définie dans config.py) est True, on passe au GameState
        if actions.get("start_game"):
            from .game_state import GameState
            self.state_manager.set_state(GameState(self.state_manager))

    def draw(self, screen):
        screen.fill((0, 0, 0))

        title_surf = self.title_font.render("Menu Principal", True, (255, 255, 255))
        info_surf = self.info_font.render("Appuyez sur ENTER pour lancer le jeu", True, (200, 200, 200))

        screen.blit(title_surf, (100, 100))
        screen.blit(info_surf, (100, 200))
