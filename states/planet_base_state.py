import os
import json
import pygame
from .base_state import BaseState
from gui.buttons import *
from config import custom_font, DEFAULT_FONT_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, ITEMS_LIST_PATH
from core.json_manager import *


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class PlanetBaseState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = custom_font
        self.inventory = self.game.data_manager.inventory
        self.tech_tree = self.game.data_manager.tech_tree.session_data


    def handle_event(self, event, pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)
        if pygame.mouse.get_pressed()[0]:
            if not self.game.spaceship.landed_planet.mines:
                if click_button('mines_buy',pos):
                    if self.inventory.has_item("mines", 1):
                        print("Mine placed")
                        self.inventory.remove_item("mines",1)
                        self.game.spaceship.landed_planet.mines =True
    def update(self, dt, actions, pos, mouse_clicked):

        pass

    def draw(self, screen, pos):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        draw_text(custom_size(13,5),"bienvenue sur cette planette",24)

        planet=self.game.spaceship.landed_planet
        planet_info=planet.planet_type
        planet_data=get_planet_data(planet_info)
        ressource=""
        for ressources in planet_data["available_ressources"]:
            quantity=""
            if ressources["spawn_rate"]<=2:
                quantity="trace de "
            elif ressources["spawn_rate"]<=4:
                quantity="presence de "
            elif ressources["spawn_rate"]<=6:
                quantity="grande quantite de "
            else:
                quantity="tres grande quantite de "
            ressource+=quantity+ressources["name"]+"\n"
        
        draw_text(custom_size(13,7),ressource,24)
        if self.tech_tree["tech_tree"]["terraforming"]["tiers"]["tier_2"]["unlocked"]:
            draw_buttons("mines_buy")
        else:
            print("tech not unlocked")


        