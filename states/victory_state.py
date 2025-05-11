import pygame
from .base_state import BaseState
from gui.buttons import *
from config import DEFAULT_FONT_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, KEY_BINDINGS, FONT_PATH


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class VictoryState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        # Charge fonts custom
        self.font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)

    def handle_event(self, event, pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["spaceship_move"]:
                from .credits_state import CreditsState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = CreditsState(self.state_manager)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

    def update(self, dt, actions, pos, mouse_clicked):
        pass

    def draw(self, screen, pos):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))
        mouse=pygame.mouse.get_pos()

        # Texte de victoire
        font = pygame.font.Font(FONT_PATH, 48)
        win_text = "Félicitations! Colonie Installée!"
        text_surf = font.render(win_text, True, (173, 255, 47))
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # Fond semi-transparent pour le message
        overlay_rect = pygame.Rect(0, text_rect.top - 20, WINDOW_WIDTH, text_rect.height + 40)
        overlay_surface = pygame.Surface(overlay_rect.size, pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 180))
        screen.blit(overlay_surface, overlay_rect.topleft)
        
        screen.blit(text_surf, text_rect)

        # Sous titre
        captain_font_size = DEFAULT_FONT_SIZE + 4
        captain_font = pygame.font.Font(FONT_PATH, captain_font_size)
        captain_text = "Bravo capitaine, vous avez sauvé l'humanité !"
        captain_surf = captain_font.render(captain_text, True, (255, 255, 255))
        captain_rect = captain_surf.get_rect(center=(WINDOW_WIDTH // 2, text_rect.bottom + 40))
        screen.blit(captain_surf, captain_rect)

        # Instruction pour voir crédits
        sub_font = pygame.font.Font(FONT_PATH, 20)
        sub_text = "Appuyez sur Espace pour voir les crédits."
        sub_surf = sub_font.render(sub_text, True, (255, 255, 255))
        # Positionner sous le message du capitaine
        sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, captain_rect.bottom + 30))
        screen.blit(sub_surf, sub_rect)
