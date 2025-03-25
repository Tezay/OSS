import pygame

from .base_state import BaseState
from gui.buttons import *
from entities.spaceship import Spaceship
import config

class GameOverState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font =  custom_font

    def handle_event(self, event, pos):
        pass

    def update(self, dt, actions, pos, mouse_clicked):
        if mouse_clicked:

            if click_button("respawn", pos):
                from states.game_state import GameState
                # Passer respawning à True pour ne pas dessiner la trajectoire
                global respawning
                config.respawning = True
                # Passer existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

                # vérification si le vaisseau est détruit (respawning = True)
                global respawning
                # Gestion du respawn reset du vaisseau
                if config.respawning:
                    print("Respawn detected ! Spaceship reset...")
                    self.game.spaceship.reset()  # Réinitialise la position du vaisseau
                    config.respawning = False  # Réinitialise la variable globale
     
            if click_button("return_menu", pos):
                from .menu_state import MenuState
                self.state_manager.set_state(MenuState(self.state_manager))
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

        # Message d'instruction
        instruction_surf = self.font.render("Vous êtes mort... Touche entrée pour réaparaître !", True, (255, 255, 255))
        instruction_rect = instruction_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(instruction_surf, instruction_rect)

        draw_buttons("respawn")
        draw_buttons("return_menu")
