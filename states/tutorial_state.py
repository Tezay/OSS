import pygame

from .base_state import BaseState
from states.game_state import GameState
from config import KEY_BINDINGS


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class TutorialState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.showing_dialogues = self.game.hud.show_dialogues

    def handle_event(self, event, pos):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["start_game"]:
                if self.showing_dialogues:
                    self.game.hud.next_dialogue()
                    self.showing_dialogues = self.game.hud.show_dialogues
                    if not self.showing_dialogues:
                        # Tuto fini
                        self.game.tutorial_completed_this_session = True
                        # Bascule sur l'état de jeu
                        self.state_manager.set_state(GameState(self.state_manager, existing_game=self.game))
            
            elif event.key == KEY_BINDINGS["exit_current_menu"]:
                # Skip le tuto
                self.game.tutorial_completed_this_session = True
                # Clear les dialogues
                self.game.hud.clear_dialogues()
                # Bascule sur l'état de jeu
                self.state_manager.set_state(GameState(self.state_manager, existing_game=self.game))

    def update(self, dt, actions, pos, mouse_clicked):
        # Jeu en pause, pas d'update
        pass

    def draw(self, screen, pos):
        # Dessine le jeu en fond
        # Passe respawning=True pour ne pas déssiner trajectoire vaisseau pendant tuto
        self.game.draw(screen, respawning=True) 
        
        # Fond semi-transparent
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Dessin des dialogues avec l'HUD
        if self.showing_dialogues:
            self.game.hud.draw_dialogues(screen)
