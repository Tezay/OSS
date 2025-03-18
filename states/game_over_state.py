from .base_state import BaseState
from buttons import *
import pygame

class GameOverState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = pygame.font.Font(None, 60)

    def handle_event(self, event, pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from .menu_state import MenuState
                self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):
        """if mouse_clicked:
            if click_button("return_to_menu", pos):
                from .menu_state import MenuState
                self.state_manager.set_state(MenuState(self.state_manager))"""
        pass

    def draw(self, screen, pos):
        # Dessine l'écran de game over
        self.game.draw(screen)  # Affiche le jeu "en fond"

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Assombrit l'écran
        screen.blit(overlay, (0, 0))

        text_surf = self.font.render("GAME OVER", True, (255, 0, 0))
        rect = text_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
        screen.blit(text_surf, rect)
"""
        # Message d'instruction
        instruction_surf = self.font.render("Appuyez sur Entrée ou cliquez pour retourner au menu", True, (255, 255, 255))
        instruction_rect = instruction_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(instruction_surf, instruction_rect)

        draw_buttons("return_to_menu")
"""