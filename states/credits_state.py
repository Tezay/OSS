import pygame
import webbrowser

from gui.buttons import *
from .base_state import BaseState
from config import FONT_PATH, DEFAULT_FONT_SIZE, WINDOW_WIDTH


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class CreditsState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

        # Polices custom
        self.title_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE + 12)
        self.names_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE + 2)

        # Liste des contributeurs (avec url pour Thomas)
        self.contributors = [
            {"name": "Eliot CUPILLARD", "url": "https://github.com/Tezay", "rect": None, "hover": False},
            {"name": "Eliot COUSSEAU", "url": "https://github.com/CSScooby", "rect": None, "hover": False},
            {"name": "Edouard TORRES", "url": "https://github.com/edouard-torres", "rect": None, "hover": False},
            {"name": "Delphine DEHEZ", "url": "https://github.com/delphine-dhz", "rect": None, "hover": False},
            {"name": "Aurélia FOURNIER", "url": "https://github.com/aurelia-f", "rect": None, "hover": False},
            {"name": "Thomas HOANG", "url": "https://www.instagram.com/thomas.hoang__/", "rect": None, "hover": False}
        ]

    def handle_event(self, event, pos):
        # Vérif si touche pour quitter appuyée
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["exit_current_menu"]:
                # Passe sur l'état MenuState
                from states.menu_state import MenuState
                self.state_manager.set_state(MenuState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):

        # Reset l'état de survol
        for contributor in self.contributors:
            contributor["hover"] = False

        # Check si la souris survol un contributeur
        for contributor in self.contributors:
            if contributor["url"] and contributor["rect"] and contributor["rect"].collidepoint(pos):
                contributor["hover"] = True
        
        # Defini les regions de clic pour les deux boutons
        button_click_width_percent = 20 
        button_click_height_percent = 5

        # Check si la souris est cliquée
        if mouse_clicked:
            # Check si le bouton retour menu est cliqué
            if click_button("menu_settings_return", pos, custom_size(button_click_width_percent, button_click_height_percent)):
                from states.menu_state import MenuState
                # Bascule sur l'état MenuState
                self.state_manager.set_state(MenuState(self.state_manager))

            # Check si le bouton GitHub est cliqué
            if click_button("git", pos, custom_size(button_click_width_percent, button_click_height_percent)):
                # Ouvre la page GitHub du projet dans le navigateur
                webbrowser.open('https://github.com/Tezay/OSS.git')

            # Check si un contributeur est cliqué
            for contributor in self.contributors:
                if contributor["url"] and contributor["rect"] and contributor["rect"].collidepoint(pos):
                    # Si un contributeur est cliqué, ouvrir son URL
                    webbrowser.open(contributor["url"])
                    break

    def draw(self, screen, pos):

        # Couleur fond
        screen.fill((10, 10, 30))

        # Dessin du titre
        title_text = "Crédits"
        title_surf = self.title_font.render(title_text, True, (200, 200, 230))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 60))
        screen.blit(title_surf, title_rect)

        # Dessin noms contributeurs
        current_y = title_rect.bottom + 45
        # Espace entre les noms
        line_spacing = self.names_font.get_height() + 15
        # Police custom
        special_title_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)

        # Itère sur chaque contributeur
        for contributor in self.contributors:
            # Check si c'est Thomas
            if contributor["name"] == "Thomas HOANG":
                # Dessine le titre spécial
                special_title_text = "Crédit spécial pour les textures du jeu"
                special_title_surf = special_title_font.render(special_title_text, True, (220, 220, 180))
                # Espacement
                current_y += line_spacing // 2
                special_title_rect = special_title_surf.get_rect(center=(WINDOW_WIDTH // 2, current_y))
                screen.blit(special_title_surf, special_title_rect)
                # Espacement
                current_y += line_spacing // 2 + 5

            # Couleur nom
            name_color = (200, 200, 200)

            # Si contributeur survolé : changer couleur
            if contributor["hover"]:
                name_color = (255, 255, 180)
            elif contributor["url"]:
                name_color = (170, 170, 255)

            # Render les noms des contributeurs
            name_surf = self.names_font.render(contributor["name"], True, name_color)
            # Centrer horizontalement
            name_rect = name_surf.get_rect(center=(WINDOW_WIDTH // 2, current_y))
            screen.blit(name_surf, name_rect)

            # Enregistre les rect des contributeurs pour detecter le clic/survol
            contributor["rect"] = name_rect

            # Ligne suivante
            current_y += line_spacing

        # Dessin des boutons
        # (voir config.py pour les coordonnées)
        button_draw_width_percent = 20
        button_draw_height_percent = 5

        
        # Dessin bouton GitHub
        git_button_config = buttons.get("git")
        draw_size_buttons("git", git_button_config["x"], git_button_config["y"], custom_size(button_draw_width_percent, button_draw_height_percent))

        # Dessin bouton retour menu
        return_button_config = buttons.get("menu_settings_return")
        draw_size_buttons("menu_settings_return", return_button_config["x"], return_button_config["y"], custom_size(button_draw_width_percent, button_draw_height_percent))




