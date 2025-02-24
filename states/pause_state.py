import pygame
from .base_state import BaseState
from config import KEY_BINDINGS

class PauseState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = pygame.font.Font(None, 50)

    def handle_event(self, event):
        # On ne regarde pas "actions", on regarde les events
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["pause"]:
                from .game_state import GameState
                new_game_state = GameState(self.state_manager)
                # On réutilise l'objet self.game (même partie) pour ne pas redémarrer la map
                new_game_state.game = self.game
                self.state_manager.set_state(new_game_state)

    def update(self, dt, actions):
        # Pas besoin de surveiller actions["pause"] ici
        pass

    def draw(self, screen):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        text_surf = self.font.render("Jeu en pause - appuyez sur P pour reprendre", True, (255, 255, 255))
        rect = text_surf.get_rect(center=screen.get_rect().center)
        screen.blit(text_surf, rect)
