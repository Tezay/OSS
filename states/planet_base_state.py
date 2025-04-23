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
class BaseState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = custom_font
        self.cell_size = 64  # Taille d'une cellule de la grille
        self.grid_margin = 10  # Espace entre les cellules
        self.grid_cols = 8  # Nombre de colonnes dans la grille
        self.item_images = self._load_item_images()

        # Calcul des coordonnées pour centrer la grille
        self.grid_width = self.grid_cols * self.cell_size + (self.grid_cols - 1) * self.grid_margin
        self.grid_x = (WINDOW_WIDTH - self.grid_width) // 2
        self.grid_y = 100  # Position verticale de la grille

    def _load_item_images(self):
        """Charge les images des items depuis items_list.json."""
        item_images = {}
        try:
            with open(ITEMS_LIST_PATH, 'r', encoding='utf-8') as file:
                items_data = json.load(file)
                for item_key, item_info in items_data.items():
                    texture_path = item_info.get("texture")
                    if texture_path and os.path.exists(texture_path):
                        item_images[item_key] = pygame.image.load(texture_path).convert_alpha()
                    else:
                        print(f"Warning: Texture not found for item '{item_key}' at path '{texture_path}'")
        except FileNotFoundError:
            print(f"Error: {ITEMS_LIST_PATH} not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to parse {ITEMS_LIST_PATH}.")
        return item_images

    def handle_event(self, event, pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

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
            #print(ressources)
            quantity=""
            if ressources["spawn_rate"]<=2:
                quantity="trace de "
            elif ressources["spawn_rate"]<=4:
                quantity="presence de "
            elif ressources["spawn_rate"]<=6:
                quantity="grande quantite de "
            else:
                pass
            ressource+=quantity+ressources["name"]+" \n "
        
        draw_text(custom_size(13,7),ressource,24)
        draw_buttons("extractor_buy")

        