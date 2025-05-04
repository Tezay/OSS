import pygame
import math

from gui.buttons import *
from config import *
from systems.planet_resources import load_item_images


# Classe pour gérer l'interface dans le jeu
class Hud:
    def __init__(self):
        self.position = (0, 0)
        self.velocity = 0
        self.fx_indicator = 0
        self.fy_indicator = 0
        self.resultant_force = 0
        self.resultant_angle = 0
        self.left_propellant = 0
        self.left_nitrogen = 0

        # Stock l'objet planète sur laquelle le vaisseau a atterri
        self.landed_planet = None
        # Charge les images des items
        self.item_images = load_item_images(scale_size=(32, 32))

        # Police de caractères pour le texte de l'HUD
        self.font = custom_font

        # Police de caractères pour les ressources de la planète atterrie (police plus petite)
        self.resource_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE - 6)

        # Chargement de la texture de la flèche directionnelle
        self.arrow_texture = pygame.image.load(DIRECTIONAL_ARROW_TEXTURE_PATH).convert_alpha()
        # Hauteur par défaut de la flèche en pixels
        default_arrow_height = 50
        # Calcul du ratio de l'aspect de la flèche
        arrow_aspect_ratio = self.arrow_texture.get_width() / self.arrow_texture.get_height()
        # Calcul de la largeur de la flèche en fonction de la hauteur et du ratio de l'aspect
        default_arrow_width = int(default_arrow_height * arrow_aspect_ratio)
        # Redimensionnement de la flèche
        self.arrow_texture = pygame.transform.scale(self.arrow_texture, (default_arrow_width, default_arrow_height))

        # Attributs pour le message d'atterrissage
        self.landing_message = ""
        # Rect pour le bouton de collecte des ressources
        self.collect_button_rect = None

        # Attributs pour les dialogues
        self.dialogues = []
        self.current_dialogue_index = -1
        self.show_dialogues = False
        self.dialogue_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)
        self.prompt_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE - 8)

    def update(self, spaceship):  # Changed signature to accept spaceship
        # Position du vaisseau
        self.position = (spaceship.x, spaceship.y)
        # Calcul de la vélocité du vaisseau
        self.velocity = math.sqrt(spaceship.vx**2 + spaceship.vy**2)
        # Calcul de la force résultante
        self.resultant_force = math.sqrt(self.fx_indicator**2 + self.fy_indicator**2)
        # Calcul de l'angle de la force résultante
        self.resultant_angle = math.degrees(math.atan2(self.fy_indicator, self.fx_indicator))
        # Mise à jour des carburants restants
        self.left_propellant = spaceship.propellant
        self.left_nitrogen = spaceship.nitrogen

        # Mise à jour de la planète atterrie
        currently_landed = spaceship.is_landed
        newly_landed_planet = spaceship.landed_planet if currently_landed else None

        # Détecter si le vaisseau vient d'atterrir
        if newly_landed_planet and not self.landed_planet:
            self.landing_message = f"Attérissage réussi sur {newly_landed_planet.name} !"
        # Si le vaisseau n'est plus atterri, effacer le message
        elif not newly_landed_planet and self.landed_planet:
            self.landing_message = ""

        # Mettre à jour l'état landed_planet pour la prochaine frame
        self.landed_planet = newly_landed_planet

        # Réinitialiser le rect du bouton si pas atterri (après avoir redécollé)
        if not self.landed_planet:
            self.collect_button_rect = None

    def load_dialogues(self, dialogues_list):
        """
        Charge une liste de dialogues à afficher.

        :param dialogues_list: Liste de chaînes de caractères (dialogues).
        """
        # Vérifie si la liste de dialogues est valide
        if dialogues_list:
            # Charge les dialogues dans l'attribut de la classe
            self.dialogues = dialogues_list
            # Passe au premier dialogue de la liste (index 0)
            self.current_dialogue_index = 0
            # Indique que les dialogues doivent être affichés
            self.show_dialogues = True
        # Si pas de dialogues, vider les attributs
        else:
            self.dialogues = []
            # Index négatif pour indiquer qu'aucun dialogue n'est affiché
            self.current_dialogue_index = -1
            # Indique que les dialogues ne doivent pas être affichés
            self.show_dialogues = False

    def next_dialogue(self):
        """Passe au dialogue suivant ou désactive l'affichage si c'est le dernier."""
        # Vérifie si l'affichage des dialogues est actif
        if self.show_dialogues:
            # Passe au dialogue suivant (incrémente index)
            self.current_dialogue_index += 1
            # Vérifie si l'index dépasse la longueur de la liste de dialogues (pour fin de liste)
            if self.current_dialogue_index >= len(self.dialogues):
                # Fin des dialogues
                self.show_dialogues = False
                self.current_dialogue_index = -1
                self.dialogues = []

    def draw_minimap(self, surface, camera, world_surface):
        """
        Dessine la mini-map en utilisant une vue réduite de la caméra.
        """
        # Définir un zoom réduit pour la mini-map
        minimap_zoom = 0.3  # Par exemple, 20% de la taille réelle

        # Obtenir une vue réduite de la caméra
        minimap_view = camera.get_custom_zoom_view(world_surface, minimap_zoom)

        # Définir la position et la taille de la mini-map sur l'écran
        minimap_width = WINDOW_WIDTH // 4.5
        minimap_height = WINDOW_HEIGHT // 4.5
        minimap_x = surface.get_width() - minimap_width - 20
        minimap_y = 20

        # Redimensionner la vue réduite pour qu'elle corresponde à la taille de la mini-map
        # Note : usage de la fonction transform.smoothscale() au lieu de transform.scale()
        # pour appliquer un filtrage bilinéaire plus doux (étoiles de fond trop petites sinon)
        minimap_surface = pygame.transform.smoothscale(minimap_view, (minimap_width, minimap_height))

        # Dessiner la bordure grise autour de la mini-map
        border_rect = pygame.Rect(minimap_x - 2, minimap_y - 2, minimap_width + 4, minimap_height + 4)
        pygame.draw.rect(surface, (128, 128, 128), border_rect)

        # Dessiner la mini-map sur la surface principale
        surface.blit(minimap_surface, (minimap_x, minimap_y))

        # Dessiner le point représentant le vaisseau
        center_x = minimap_x + minimap_width // 2
        center_y = minimap_y + minimap_height // 2
        pygame.draw.circle(surface, (255, 0, 0), (center_x, center_y), 2)

    def draw_landed_planet_resources(self, surface):
        """Dessine la liste des ressources de la planète atterrie sur le côté droit, avec un fond."""
        if not self.landed_planet:
            # Repasse le rect à None si pas atterri (redécollé)
            self.collect_button_rect = None
            return

        # Définition des constantes

        # Position X de départ pour le contenu (texte, images)
        start_x = WINDOW_WIDTH - 375
        # Position Y de départ pour le contenu
        start_y = WINDOW_HEIGHT // 2 - 100
        # Hauteur de ligne pour chaque ressource
        line_height = 40
        # Marge intérieure autour du contenu dans le fond
        padding = 10
        # Largeur pour l'image de l'item
        item_image_width = 32
        # Estimation large pour la largeur max du texte (nom + quantité)
        estimated_text_width = 300
        # Hauteur du bouton "Récupérer les items"
        button_height = 40
        # Espace entre la liste et le bouton
        button_padding_top = 20

        # Calcul de la taille nécessaire pour le fond

        # Largeur du fond = Largeur image + Marge + Largeur texte estimée + Marge
        bg_width = item_image_width + padding + estimated_text_width + padding

        # Hauteur du titre
        title_height = 30

        # Nombre de ressources à afficher
        num_resources = len(self.landed_planet.resources)

        # Hauteur totale du fond = Marge + Hauteur titre + Marge + (Nb ressources * Hauteur ligne) + Espace bouton + Hauteur bouton + Marge
        bg_height = (padding + title_height + padding + (num_resources * line_height) + button_padding_top + button_height + padding)

        # Création et dessin du fond

        # Créer une surface distincte pour le fond avec transparence alpha
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        # Remplissage de la surface avec une couleur semi-transparente
        bg_surface.fill((0, 0, 0, 80))
        # Dessiner de la surface de fond sur l'écran principal
        surface.blit(bg_surface, (start_x - padding, start_y - padding))

        # Dessin du contenu (par-dessus le fond)

        # Position Y actuelle pour dessiner les éléments (commence à start_y)
        current_y = start_y

        # Dessiner le titre
        title_text = "Resources disponibles :"
        title_surf = self.font.render(title_text, True, (255, 255, 255))
        surface.blit(title_surf, (start_x, current_y))
        # Avancer la position Y après le titre et un petit espace
        current_y += title_height + padding

        # Dessiner chaque ressource
        sorted_resource_names = sorted(self.landed_planet.resources.keys())
        for resource_name in sorted_resource_names:
            quantity = self.landed_planet.resources[resource_name]
            # Position X pour l'image et le texte de cette ligne
            current_x = start_x

            # Dessiner l'image de la ressource
            if resource_name in self.item_images:
                img = self.item_images[resource_name]
                surface.blit(img, (current_x, current_y))
                img_width = img.get_width()
            else: # Si pas d'image, dessiner un carré gris
                pygame.draw.rect(surface, (100, 100, 100), (current_x, current_y, 32, 32))
                img_width = 32
            # Décaler X pour le texte, après l'image et une marge
            current_x += img_width + padding

            # Dessiner le nom et la quantité
            resource_text = f"{resource_name} : {quantity:.0f}"
            resource_surf = self.resource_font.render(resource_text, True, (255, 255, 255))
            # Centrer verticalement le texte par rapport à l'image
            text_y_offset = (32 - resource_surf.get_height()) // 2
            surface.blit(resource_surf, (current_x, current_y + text_y_offset))

            # Passer à la ligne suivante pour la prochaine ressource
            current_y += line_height

        # Dessin du bouton "Récupérer les ressources"

        # Position Y du bouton = Position Y après la liste + marge
        button_y = current_y + button_padding_top
        # Position X du bouton = Position X de départ du contenu
        button_x = start_x
        # Même largeur que le fond
        button_width = bg_width

        # Créer le rectangle du bouton pour la détection de clic et le dessin
        self.collect_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Couleur de fond du bouton (change si survolé)
        button_color = (80, 80, 120) # Couleur de base
        mouse_pos = pygame.mouse.get_pos()
        if self.collect_button_rect.collidepoint(mouse_pos):
            button_color = (100, 100, 150) # Couleur plus claire au survol

        # Dessiner le fond du bouton
        pygame.draw.rect(surface, button_color, self.collect_button_rect)
        # Dessiner une bordure autour du bouton
        pygame.draw.rect(surface, (200, 200, 200), self.collect_button_rect, 2)

        # Dessiner le texte du bouton
        button_text = "Récupérer les ressources"
        button_text_surf = self.resource_font.render(button_text, True, (255, 255, 255))
        button_text_rect = button_text_surf.get_rect(center=self.collect_button_rect.center)
        surface.blit(button_text_surf, button_text_rect)

    def draw_dialogue(self, surface):
        """Dessine le dialogue actuel si l'affichage est actif."""
        if self.show_dialogues and 0 <= self.current_dialogue_index < len(self.dialogues):
            dialogue_text = self.dialogues[self.current_dialogue_index]
            
            # Paramètres d'affichage
            # Fond noir semi-transparent
            dialogue_bg_color = (0, 0, 0, 75)
            # Couleur texte blanc
            dialogue_text_color = (255, 255, 255)
            # Couleur texte gris clair (pour le texte "Appuyer sur [Entrée]...")
            prompt_text_color = (200, 200, 200)
            # Marge pour le fond
            padding = 15
            # Marge par rapport au bas de l'écran (pour laisser la place à l'HUD)
            bottom_margin = 200
            # Marge entre dialogue et texte "Appuyer sur [Entrée]..."
            prompt_margin_top = 5

            # Rendu du texte principal
            text_surface = self.dialogue_font.render(dialogue_text, True, dialogue_text_color)
            text_rect = text_surface.get_rect()

            # Calcul de la taille et position du fond
            # Largeur et hauteur du fond = largeur et hauteur du texte + 2*marges (pour marge à gauche et droite)
            bg_width = text_rect.width + 2 * padding
            bg_height = text_rect.height + 2 * padding
            # Position du fond
            bg_x = (surface.get_width() - bg_width) // 2
            bg_y = surface.get_height() - bottom_margin - bg_height

            # Création et dessin du fond
            bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            bg_surface.fill(dialogue_bg_color)
            surface.blit(bg_surface, (bg_x, bg_y))

            # Positionnement et dessin du texte sur le fond
            text_rect.center = (bg_x + bg_width // 2, bg_y + bg_height // 2)
            surface.blit(text_surface, text_rect)

            # Rendu et dessin du texte "Appuyer sur [Entrée]..."
            prompt_text = "Appuyer sur [Entrée] pour continuer"
            prompt_surface = self.prompt_font.render(prompt_text, True, prompt_text_color)
            prompt_rect = prompt_surface.get_rect()
            # Positionner le petit texte en dessous à droite du dialogue
            prompt_rect.topright = (bg_x + bg_width, bg_y + bg_height + prompt_margin_top)
            surface.blit(prompt_surface, prompt_rect)

    def draw(self, surface, camera, world_surface, world_surface_wiouth_stars):
        """
        Dessine l'HUD.
        """

        # Récupère les coordonnées de la grille
        # Affiche la grille si DEBUG_MODE = True
        coord = grille(DEBUG_MODE)

        # Création des textes à afficher
        position_text = f"Position: x: {self.position[0]:.2f}, y: {self.position[1]:.2f}"
        velocity_text = f"Velocity: {self.velocity:.2f}"
        forces_text = f"Spaceship resultant force: {self.resultant_force:.2f}"
        left_nitrogen_text = f"Nitrogen: {self.left_nitrogen:.2f}"
        left_propellant_text = f"Propellant: {self.left_propellant:.2f}"

        # Création des surfaces de texte
        position_surface = self.font.render(position_text, True, (255, 255, 255))
        velocity_surface = self.font.render(velocity_text, True, (255, 255, 255))
        forces_surface = self.font.render(forces_text, True, (255, 255, 255))
        left_nitrogen_surface = self.font.render(left_nitrogen_text, True, (255, 255, 255))
        left_propellant_surface = self.font.render(left_propellant_text, True, (255, 255, 255))

        # Affichage des textes à l'écran

        # surface.blit(position_surface, (20, 20))
        # surface.blit(velocity_surface, (20, 50))
        # surface.blit(forces_surface, (20, 80))
        # surface.blit(left_nitrogen_surface, (20, 110))
        # surface.blit(left_propellant_surface, (20, 140))

        # Dessin de l'HUD
        coord_hud = hud_draw(10, 30, 50, 35)
        # print(coord_hud)
        image = pygame.image.load('assets/hud/main_hud.png')

        # Calcule la taille de l'image de fond de l'HUD (et la redimensionne)
        lenght, height = coord_hud[2], coord_hud[3]
        image = pygame.transform.scale(image, (lenght, height))

        # Affichage de l'image de fond de l'HUD
        screen.blit(image, coord_hud)

        # Dessin de la mini-map
        self.draw_minimap(surface, camera, world_surface_wiouth_stars)

        # Dessiner la flèche directionnelle de la force résultante
        arrow_x = custom_size(20, 32)[0]
        arrow_y = custom_size(20, 32)[1]
        # Rotation de la flèche pour pointer dans la direction de la force résultante (+270 pour l'angle initial de la flèche)
        rotated_arrow = pygame.transform.rotate(self.arrow_texture, -self.resultant_angle + 270)
        arrow_rect = rotated_arrow.get_rect(center=(arrow_x + self.arrow_texture.get_width() // 2, arrow_y + self.arrow_texture.get_height() // 2))
        surface.blit(rotated_arrow, arrow_rect.topleft)

        draw_buttons("game_settings", (30, 30))
        draw_buttons("tech_tree", (30, 30))
        draw_buttons("inventory", (30, 30))
        propelent = left_propellant_text[11:] + str("/50")
        draw_text(custom_size(34.25, 31.25), propelent)
        nitrogen = left_nitrogen_text[9:] + str("/20")
        draw_text(custom_size(34.25, 33.25), nitrogen)
        # print(position_text)
        position_x = position_text[9:17]
        draw_text(custom_size(13, 31), position_x)
        position_y = position_text[21:29]
        draw_text(custom_size(13, 31.75), position_y)
        draw_text(custom_size(13, 33), velocity_text)

        # Draw landing message if it exists
        if self.landing_message:
            message_surf = self.font.render(self.landing_message, True, (255, 255, 255))
            message_rect = message_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 200))  # Positioned bottom-center
            surface.blit(message_surf, message_rect)

        # Dessine la liste des ressources et le bouton si applicable
        if self.landed_planet:
            self.draw_landed_planet_resources(surface)
        else:
            # S'assurer que le rect est None si pas atterri
            self.collect_button_rect = None

        # Dessiner le dialogue actuel si nécessaire
        self.draw_dialogue(surface)












