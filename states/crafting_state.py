import os
import pygame
from .base_state import BaseState
from gui.buttons import *
from config import custom_font, DEFAULT_FONT_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, ITEMS_LIST_PATH, KEY_BINDINGS
from core.json_manager import get_crafting_recipes, get_items_data

# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class CraftingState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = custom_font
        self.inventory = self.game.data_manager.inventory
        # Charger les images des items
        self.item_images = self._load_item_images()
        # Charger les données de tous les items (pour noms/descriptions)
        self.all_items_data = get_items_data()
        # Charger les craft recipes
        self.crafting_recipes = get_crafting_recipes()

        # Variables pour l'interface
        # Zone pour la liste des items de l'inventaire
        self.list_area_rect = pygame.Rect(50, 80, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT - 160)
        # Zone pour les items sélectionnés
        self.selected_area_rect = pygame.Rect(self.list_area_rect.right + 50, 80, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.5)
        # Zone pour le résultat du craft
        self.result_area_rect = pygame.Rect(self.selected_area_rect.left, self.selected_area_rect.bottom + 20, self.selected_area_rect.width, WINDOW_HEIGHT * 0.3)
        # Coordonnées pour le début de la liste des items (+10 pour le padding)
        self.item_list_start_y = self.list_area_rect.top + 10
        # Espacement entre les items dans la liste
        self.item_list_spacing = 40
        # Taille des images d'items dans la liste
        self.item_image_size = (32, 32)

        #Variables pour la logique de craft
        # Dictionnaire {item_name: quantity} des items sélectionnés pour le craft
        self.selected_items = {}
        # Dictionnaire pour stocker les Rect de chaque item dans la liste
        self.inventory_clickable_rects = {}
        # Stock la recipe correspondante si un craft est possible
        self.possible_craft = None
        # Rect du bouton "Assembler"
        self.craft_button_rect = None

    def _load_item_images(self):
        """Charge les images des items depuis items_list.json."""
        item_images = {}
        try:
            # Charger les données des items depuis le fichier JSON
            items_data = get_items_data()
            # Itère sur chaque item pour charger son image
            for item_key, item_info in items_data.items():
                texture_path = item_info.get("texture")
                if texture_path and os.path.exists(texture_path):
                    try:
                        # Charger l'image et la convertir
                        img = pygame.image.load(texture_path).convert_alpha()
                        # Redimensionner si nécessaire pour l'affichage dans la liste
                        img = pygame.transform.scale(img, self.item_image_size)
                        item_images[item_key] = img
                    except:
                         print(f"Warning: Failed to load or scale image for item '{item_key}' at path '{texture_path}'.")
        except Exception as e:
            print(f"Error loading item images: {e}")
        return item_images

    def handle_event(self, event, pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:
            # Quitter le menu craft avec Echap ou la touche de craft
            if event.key == KEY_BINDINGS["exit_current_menu"] or event.key == KEY_BINDINGS["crafting"]:
                self._exit_state()

        # Vérifier si la souris est cliquée
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifie si c'est un clic gauche
            if event.button == 1:
                # Vérifier clic sur un item de l'inventaire (parcourt chaque rect)
                for item_name, rect in self.inventory_clickable_rects.items():
                    # Si le clic est dans le rect de l'item
                    if rect.collidepoint(pos):
                        # Toggle l'item sélectionné
                        self._toggle_item_selection(item_name)
                        # Sortir après avoir trouvé l'item cliqué
                        break

                # Vérifier clic sur le bouton "Retour"
                if click_button("crafting_return", pos):
                     self._exit_state()

                # Vérifier clic sur le bouton "Assembler"
                if self.possible_craft and self.craft_button_rect and self.craft_button_rect.collidepoint(pos):
                    self._perform_craft()


    def _exit_state(self):
        """Quitte l'état CraftingState pour retourner à GameState."""
        from .game_state import GameState
        # Passer existing_game=self.game pour réutiliser l’instance
        new_game_state = GameState(self.state_manager, existing_game=self.game)
        # Change l'état courant à GameState
        self.state_manager.set_state(new_game_state)

    def _toggle_item_selection(self, item_name):
        """Ajoute ou retire un item de la sélection pour le craft."""
        if item_name in self.selected_items:
            # Si déjà sélectionné, le retirer de la sélection
            del self.selected_items[item_name]
            print(f"Removed {item_name} from selection.")
        else:
            # Sinon, on l'ajoute (vérifie qu'il est dans l'inventaire, au moins 1)
            if self.inventory.has_item(item_name, 1):
                # Stocker l'item sélectionné
                self.selected_items[item_name] = 1
                print(f"Added {item_name} to selection.")

        # Après modification de la sélection, vérifier si craft possible
        self._check_crafting_recipe()

    def _check_crafting_recipe(self):
        """Vérifie si les items sélectionnés correspondent à une recipe."""
        # Réinitialiser la liste des recipes possibles
        self.possible_craft = None
        # Créer un set des noms d'items sélectionnés (pour pas de doublons)
        selected_item_names = set(self.selected_items.keys())

        # Vérifier si la sélection est vide
        if not selected_item_names:
            return False

        # Itère sur chaque recipe de craft
        for recipe in self.crafting_recipes:
            # Récupérer les items nécessaires pour la recipe
            required_ingredients = recipe.get("ingredients", [])
            # Créer un set des noms d'items requis pour la recipe
            recipe_ingredient_names = set()
            for ingredient in required_ingredients:
                recipe_ingredient_names.add(ingredient["name"])

            # Vérifier si les noms des items sélectionnés correspondent exactement aux noms de la recipe
            if selected_item_names == recipe_ingredient_names:
                # Vérifier si les quantités dans l'inventaire sont suffisantes pour cette recipe
                has_enough_ingredients = True
                for ingredient in required_ingredients:
                    item_name = ingredient["name"]
                    required_quantity = ingredient["quantity"]
                    if not self.inventory.has_item(item_name, required_quantity):
                        has_enough_ingredients = False
                        # Pas la peine de vérifier les autres items pour cette recipe
                        break 

                # Si tous les items sont présents en quantité suffisante
                if has_enough_ingredients:
                    # Stock la recette trouvée
                    self.possible_craft = recipe
                    print(f"Possible craft found: {recipe['result']['name']}")
                    # Return True dès qu'une recipe valide est trouvée
                    return True

        # Si aucune recuoe n'a correspondu après la boucle
        if not self.possible_craft:
             print("No matching recipe found for selected items.")
        return False

    def _perform_craft(self):
        """Exécute le craft si possible."""
        # Vérifier si une recette possible a été trouvée
        if not self.possible_craft:
            print("Crafting error: No valid recipe selected.")
            return

        # Récupérer la recipe possible
        recipe = self.possible_craft
        ingredients = recipe.get("ingredients", [])
        result = recipe.get("result")

        # Re-vérification finale des quantités
        can_craft = True
        for ingredient in ingredients:
            if not self.inventory.has_item(ingredient["name"], ingredient["quantity"]):
                can_craft = False
                print(f"Crafting failed: Not enough {ingredient['name']}.")
                break

        # Si tous les ingrédients sont présents en quantité suffisante
        if can_craft and result:
            # Retirer les ingrédients de l'inventaire
            for ingredient in ingredients:
                self.inventory.remove_item(ingredient["name"], ingredient["quantity"])
                print(f"Used {ingredient['quantity']}x {ingredient['name']}")

            # Ajouter le résultat à l'inventaire
            self.inventory.add_item(result["name"], result["quantity"])
            print(f"Crafted {result['quantity']}x {result['name']}")

            # Réinitialiser la sélection et la recipe possible
            self.selected_items = {}
            self.possible_craft = None

        else:
            print("Crafting failed.")


    def update(self, dt, actions, pos, mouse_clicked):
        pass


    def draw(self, screen, pos):
        # Dessiner le fond (jeu + overlay sombre)
        self.game.draw(screen)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Dessiner les zones principales (pour le debug)
        if DEBUG_MODE:
            pygame.draw.rect(screen, (50, 0, 0), self.list_area_rect, 2)
            pygame.draw.rect(screen, (0, 50, 0), self.selected_area_rect, 2)
            pygame.draw.rect(screen, (0, 0, 50), self.result_area_rect, 2)

        # Dessiner la liste des items de l'inventaire à gauche
        # Vider la liste des rects avant de redessiner
        self.inventory_clickable_rects.clear()
        # Récupérer la coordonnée Y de départ pour la liste
        current_y = self.item_list_start_y
        # Récupérer les items de l'inventaire (liste de dictionnaires)
        inventory_items = self.inventory.get_inventory()

        # Titre de la liste
        title_surf = self.font.render("Inventaire", True, (255, 255, 255))
        screen.blit(title_surf, (self.list_area_rect.left + 10, self.list_area_rect.top - 30))

        # Itère sur chaque item de l'inventaire
        for item in inventory_items:
            # Récupérer le nom et la quantité de l'item
            item_name = item["name"]
            item_quantity = item["quantity"]

            # Position de cet item dans la liste
            item_rect = pygame.Rect(self.list_area_rect.left + 10, current_y, self.list_area_rect.width - 20, self.item_list_spacing - 5)
            # Stocker le rect pour la détection de clic
            self.inventory_clickable_rects[item_name] = item_rect

            # Couleur de fond si sélectionné
            if item_name in self.selected_items:
                bg_color = (80, 80, 80)
            else:
                bg_color = (40, 40, 40)
            pygame.draw.rect(screen, bg_color, item_rect)

            # Récupérer la position de l'image de l'item
            img_pos = (item_rect.left + 5, item_rect.centery - self.item_image_size[1] // 2)
            # Vérifier si l'image de l'item existe
            if item_name in self.item_images:
                # Dessiner l'image de l'item
                screen.blit(self.item_images[item_name], img_pos)
            # Sinon : dessiner carré gris
            else:
                 pygame.draw.rect(screen, (100, 100, 100), (img_pos[0], img_pos[1], self.item_image_size[0], self.item_image_size[1]), 1)

            # Dessiner le nom et la quantité
            item_info_text = f"{self.all_items_data.get(item_name, {}).get('name', item_name)} ({item_quantity})"
            text_surf = self.font.render(item_info_text, True, (255, 255, 255))
            text_pos = (img_pos[0] + self.item_image_size[0] + 10, item_rect.centery - text_surf.get_height() // 2)
            screen.blit(text_surf, text_pos)

            # Passer la coordonnée Y à la ligne suivante
            current_y += self.item_list_spacing

            # Arrêter si dépasse la zone
            if current_y + self.item_list_spacing > self.list_area_rect.bottom:
                break

        # Dessiner les items sélectionnés
        selected_title_surf = self.font.render("Ressources Sélectionnées", True, (255, 255, 255))
        screen.blit(selected_title_surf, (self.selected_area_rect.left + 10, self.selected_area_rect.top - 30))

        # Dessiner un fond pour la zone des ingrédients
        pygame.draw.rect(screen, (30, 30, 30), self.selected_area_rect)

        # Afficher les images des items sélectionnés
        selected_x = self.selected_area_rect.left + 15
        selected_y = self.selected_area_rect.top + 15
        max_x = self.selected_area_rect.right - self.item_image_size[0] - 15

        for item_name in self.selected_items.keys():
            if item_name in self.item_images:
                screen.blit(self.item_images[item_name], (selected_x, selected_y))
                # Décaler pour le suivant
                selected_x += self.item_image_size[0] + 10
                # Retour à la ligne si dépasse la zone
                if selected_x > max_x:
                    selected_x = self.selected_area_rect.left + 15
                    selected_y += self.item_image_size[1] + 10

        # Dessiner le résultat possible du craft
        result_title_surf = self.font.render("Résultat", True, (255, 255, 255))
        screen.blit(result_title_surf, (self.result_area_rect.left + 10, self.result_area_rect.top - 30))
        # Dessiner un fond pour la zone de résultat
        pygame.draw.rect(screen, (30, 30, 30), self.result_area_rect)

        # Afficher le résultat du craft si possible
        if self.possible_craft:
            # Récupérer le nom et la quantité du résultat
            result_item = self.possible_craft["result"]
            result_name = result_item["name"]
            result_quantity = result_item["quantity"]

            # Afficher l'image du résultat (sinon carré gris)
            res_img_pos = (self.result_area_rect.left + 15, self.result_area_rect.top + 15)
            if result_name in self.item_images:
                 screen.blit(self.item_images[result_name], res_img_pos)
            else:
                 pygame.draw.rect(screen, (100, 100, 100), (res_img_pos[0], res_img_pos[1], self.item_image_size[0], self.item_image_size[1]), 1)

            # Afficher le nom et la quantité du résultat
            result_info_text = f"{self.all_items_data.get(result_name, {}).get('name', result_name)} (x{result_quantity})"
            res_text_surf = self.font.render(result_info_text, True, (255, 255, 255))
            res_text_pos = (res_img_pos[0] + self.item_image_size[0] + 10, res_img_pos[1] + self.item_image_size[1]//2 - res_text_surf.get_height() // 2)
            screen.blit(res_text_surf, res_text_pos)

            # Récupérer les données du bouton "Assembler" depuis le fichier de config
            button_data = buttons.get("craft_button")
            # Si bouton existe
            if button_data:
                # Positionner le bouton dans la zone de résultat
                btn_width_px = (WINDOW_WIDTH / 50) * button_size_widht
                btn_height_px = (WINDOW_HEIGHT / 35) * button_size_height
                btn_x = self.result_area_rect.centerx - btn_width_px // 2
                btn_y = self.result_area_rect.bottom - btn_height_px - 15
                # Dessiner le bouton "Assembler"
                self.craft_button_rect = draw_button_manual(screen, button_data, btn_x, btn_y, btn_width_px, btn_height_px)
                temp_rect = pygame.Rect(btn_x, btn_y, btn_width_px, btn_height_px)
                pygame.draw.rect(screen, button_data.get("color", (0, 200, 0)), temp_rect)
                btn_text_surf = self.font.render(button_data.get("text", "Assembler"), True, (0, 0, 0))
                screen.blit(btn_text_surf, btn_text_surf.get_rect(center=temp_rect.center))
                # Stock le rect du bouton pour la détection de clic
                self.craft_button_rect = temp_rect
            ## Sinon : pas de craft possible, pas de bouton
            else:
                self.craft_button_rect = None

        # Dessiner bouton retour
        draw_buttons("crafting_return")

        # Titre de l'écran
        title_surf = self.font.render("Zone d'Assemblage", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 40))
        screen.blit(title_surf, title_rect)