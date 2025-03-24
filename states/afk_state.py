import pygame
from .base_state import BaseState
import config

class AFKState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = pygame.font.Font(None, 60)

    def handle_event(self, event, pos):
        # Si le joueur appuie sur une touche ou clique, il sort de l'AFK
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            from states.game_state import GameState
            new_game_state = GameState(self.state_manager, existing_game=self.game)
            self.state_manager.set_state(new_game_state)

    def update(self, dt, actions, pos, mouse_clicked):
        pass
    
    def draw(self, screen, pos):
        # Affiche le jeu en arrière-plan
        self.game.draw(screen)

        # Crée une couche sombre par-dessus l'écran
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Affiche le message "AFK"
        text_surf = self.font.render("Vous êtes passé en AFK", True, (255, 0, 0))
        rect = text_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
        screen.blit(text_surf, rect)

        # Instruction pour revenir en jeu
        instruction_surf = self.font.render("Cliquez ou appuyez sur une touche pour continuer", True, (255, 255, 255))
        instruction_rect = instruction_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(instruction_surf, instruction_rect)
