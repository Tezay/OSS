import os
import json
import pygame
from .base_state import BaseState
from gui.buttons import *
from config import custom_font, DEFAULT_FONT_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, ITEMS_LIST_PATH


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class InventoryState(BaseState):
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
            if event.key == KEY_BINDINGS["inventory"] or event.key == KEY_BINDINGS["exit_current_menu"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

    def update(self, dt, actions, pos, mouse_clicked):
        
        if mouse_clicked:
            ########### TEST ############
            # Exemple de bouton pour tester l'ajout/suppression d'un item dans l'inventaire
            if click_button('test_add_item',pos):
                self.game.data_manager.inventory.add_item("liquid_water", 2)
            if click_button('test_remove_item',pos):
                self.game.data_manager.inventory.remove_item("liquid_water", 2)
            #############################

    def draw(self, screen, pos):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        mouse=pygame.mouse.get_pos()

        position_save={}
        # On parcourt chaque item de l'inventaire en utilisant son index
        for index, item in enumerate(self.game.data_manager.inventory.get_inventory()):
            # Calcul de la colonne actuelle dans la grille (modulo du nombre de colonnes)
            col = index % self.grid_cols
            # Calcul de la ligne actuelle dans la grille (division entière par le nombre de colonnes)
            row = index // self.grid_cols
            # Calcul de la position horizontale (x) de la cellule dans la grille
            x = self.grid_x + col * (self.cell_size + self.grid_margin)
            # Calcul de la position verticale (y) de la cellule dans la grille
            y = self.grid_y + row * (self.cell_size + self.grid_margin)
            # Dessine un rectangle représentant une cellule de la grille
            pygame.draw.rect(screen, (50, 50, 50), (x, y, self.cell_size, self.cell_size))
            # Vérifie si l'item a une image associée dans le dictionnaire des images d'items
            position_save[item["name"]] = (x, y)

            if item["name"] in self.item_images:
                # Si une image est trouvée, elle est dessinée dans la cellule correspondante
                screen.blit(self.item_images[item["name"]], (x, y))
                # Dessine la quantité de l'item dans le coin inférieur droit de la cellule
                quantity_text = self.font.render(str(item["quantity"]), True, (255, 255, 255))
                screen.blit(quantity_text, (x + self.cell_size - 20, y + self.cell_size - 20))  

        #print("Position de l'item dans l'inventaire :", position_save)
        
        items_list = self.game.data_manager.inventory.get_items_data()
        for key, item in items_list.items():
            # Récupération de la position de l'item dans l'inventaire
            if key in position_save:
                x = position_save[key][0]
                y = position_save[key][1]
                # Dessin de l'item à la position correspondante
                txt=item["name"]+" \n \n "+item["description"]
                colide_draw_coord(txt, mouse, x, y,self.cell_size)


        #print("Position de l'item dans l'inventaire :", position_save)
        
        # Dessin du texte
        text_surf = self.font.render("Inventaire - appuyez sur I pour reprendre", True, (255, 255, 255))
        rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, 50))

        ########### TEST ############
        # Exemple de bouton pour tester l'upgrade d'un module du tech tree
        draw_buttons("test_add_item")
        draw_buttons("test_remove_item")
        #############################

        


        screen.blit(text_surf, rect)
