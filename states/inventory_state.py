import os
import json
import pygame
from .base_state import BaseState
from gui.buttons import *
from config import custom_font, DEFAULT_FONT_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, ITEMS_LIST_PATH, KEY_BINDINGS, SPACESHIP_MAX_NITROGEN, SPACESHIP_MAX_PROPELLANT, FONT_PATH


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
        # Charge fonts custom
        self.font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)
        self.quantity_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE - 8)
        
        # Taille d'une cellule de la grille
        self.cell_size = 64
        # Espace entre les cellules
        self.grid_margin = 10
        # Nombre de colonnes dans la grille
        self.grid_cols = 8
        # Charge les images des items
        self.item_images = self._load_item_images()
        # Dico pour stocker les Rect des items dans la grille pour la détection de clic
        self.inventory_clickable_rects = {}

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

        # Gestion des clics sur les items de l'inventaire
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Vérif clic gauche
            if event.button == 1:
                # Itère sur chaque rects des items de l'inventaire
                for item_name, rect in self.inventory_clickable_rects.items():
                    # Vérifie si le clic est à l'intérieur du rect de l'item
                    if rect.collidepoint(pos):
                        print(f"Clicked on item: {item_name}")
                        self.game.sound_manager.play_sound("use_item", "use_item.wav")
                        # Recharge fuel neutral_gas
                        if item_name == "neutral_gas":
                            # Check si le joueur a l'item avant de le retirer
                            if self.game.data_manager.inventory.has_item(item_name, 1):
                                # Retire l'item de l'inventaire
                                if self.game.data_manager.inventory.remove_item(item_name, 1):
                                    current_nitrogen = self.game.spaceship.nitrogen
                                    add_nitrogen = 1.0
                                    new_nitrogen = min(current_nitrogen + add_nitrogen, SPACESHIP_MAX_NITROGEN)
                                    self.game.spaceship.nitrogen = new_nitrogen
                                    print(f"Refilled Nitrogen. Current: {new_nitrogen:.2f}/{SPACESHIP_MAX_NITROGEN}")
                                else:
                                    print(f"Failed to remove {item_name}.")
                            else:
                                print(f"Not enough {item_name} to refuel.")

                        # Recharge fuel hydrogen_gas
                        elif item_name == "hydrogen_gas":
                            # Check si le joueur a l'item avant de le retirer
                            if self.game.data_manager.inventory.has_item(item_name, 1):
                                # Retire l'item de l'inventaire
                                if self.game.data_manager.inventory.remove_item(item_name, 1):
                                    current_propellant = self.game.spaceship.propellant
                                    add_propellant = 5.0
                                    new_propellant = min(current_propellant + add_propellant, SPACESHIP_MAX_PROPELLANT)
                                    self.game.spaceship.propellant = new_propellant
                                    print(f"Refilled Propellant. Current: {new_propellant:.2f}/{SPACESHIP_MAX_PROPELLANT}")
                                else:
                                    print(f"Failed to remove {item_name}.")
                            else:
                                print(f"Not enough {item_name} to refuel.")

                        # Break si un item est cliqué
                        break

    def update(self, dt, actions, pos, mouse_clicked):
        pass

    def draw(self, screen, pos):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        mouse=pygame.mouse.get_pos()

        position_save={}
        # Vide dictonnaire des rects cliquables avant de redessiner
        self.inventory_clickable_rects.clear()
        
        # Liste pour stocker les informations nécessaires au dessin des quantités
        items_to_draw_quantities = []

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
            item_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            # Dessin du fond de la cellule
            pygame.draw.rect(screen, (50, 50, 50), item_rect, border_radius=10)
            
            # Stock les coordonnées de l'item dans le dictionnaire pour la détection de clics
            self.inventory_clickable_rects[item["name"]] = item_rect
            # Sauvegarde la position pour l'affichage des descriptions
            position_save[item["name"]] = (x, y)

            # Vérifie si l'item a une image associée dans le dico des images d'items
            if item["name"] in self.item_images:
                # Si une image est trouvée, elle est dessinée dans la cellule correspondante
                screen.blit(self.item_images[item["name"]], (x, y))
            
            # Ajoute l'item et sa quantité à la liste
            items_to_draw_quantities.append({'rect': item_rect, 'quantity': item["quantity"]})

        # Dessiner les quantités par dessus
        for item_info in items_to_draw_quantities:
            item_rect = item_info['rect']
            quantity = item_info['quantity']
            
            # Dessine la quantité de l'item dans le coin inférieur droit de la cellule
            quantity_text_surface = self.quantity_font.render(str(quantity), True, (255, 255, 255))
            # Positionnement texte en bas à droite de la cellule
            text_rect = quantity_text_surface.get_rect(bottomright=(item_rect.right - 5, item_rect.bottom - 5))
            screen.blit(quantity_text_surface, text_rect)
        
        items_list = self.game.data_manager.inventory.get_items_data()
        for key, item in items_list.items():
            # Récupération de la position de l'item dans l'inventaire
            if key in position_save:
                x = position_save[key][0]
                y = position_save[key][1]
                # Dessin de l'item à la position correspondante
                txt=item["name"]+" \n \n "+item["description"]
                colide_draw_coord(txt, mouse, x, y,self.cell_size)
        
        # Dessin du texte
        text_surf = self.font.render("Inventaire - appuyez sur I pour reprendre", True, (255, 255, 255))
        rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, 50))
        
        screen.blit(text_surf, rect)
