import pygame
import math
import os
import time

from gui.buttons import *
from config import *
from systems.planet_resources import load_item_images
from core.json_manager import get_dialogues
from states.tech_tree_state import TechTreeState

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
        # Police pour les textes des contrôles
        self.controls_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE - 10)

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
        # Rect pour le bouton "installer colonie"
        self.install_colony_button_rect = None

        # Attributs pour les dialogues
        self.dialogues = []
        self.current_dialogue_index = -1
        self.show_dialogues = False
        self.dialogue_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)
        self.prompt_font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE - 8)

        # Chargement des images des touches pour l'affichage des contrôles
        key_img_path = "assets/key/"
        try:
            self.key_q_img = pygame.image.load(os.path.join(key_img_path, "q_key.png")).convert_alpha()
            self.key_d_img = pygame.image.load(os.path.join(key_img_path, "d_key.png")).convert_alpha()
            self.key_space_img = pygame.image.load(os.path.join(key_img_path, "space_key.png")).convert_alpha()
            self.key_i_img = pygame.image.load(os.path.join(key_img_path, "i_key.png")).convert_alpha()
            self.key_c_img = pygame.image.load(os.path.join(key_img_path, "c_key.png")).convert_alpha()
            self.key_m_img = pygame.image.load(os.path.join(key_img_path, "m_key.png")).convert_alpha()
            self.key_t_img = pygame.image.load(os.path.join(key_img_path, "t_key.png")).convert_alpha()
            self.key_esc_img = pygame.image.load(os.path.join(key_img_path, "escape_key.png")).convert_alpha()
           
            # Redimensionnement des images des touches
            key_size = (30, 30)
            space_key_height = 30
            space_key_width = 130
            self.key_q_img = pygame.transform.scale(self.key_q_img, key_size)
            self.key_d_img = pygame.transform.scale(self.key_d_img, key_size)
            self.key_i_img = pygame.transform.scale(self.key_i_img, key_size)
            self.key_c_img = pygame.transform.scale(self.key_c_img, key_size)
            self.key_m_img = pygame.transform.scale(self.key_m_img, key_size)
            self.key_t_img = pygame.transform.scale(self.key_t_img, key_size)
            self.key_esc_img = pygame.transform.scale(self.key_esc_img, key_size)
            self.key_space_img = pygame.transform.scale(self.key_space_img, (space_key_width, space_key_height))

        except pygame.error as e:
            print(f"Error while charing key texture : {e}")

        # Liste des boites d'info
        self.info_boxes = []
        # Police des boites d'info
        self.info_box_font = pygame.font.Font(FONT_PATH, INFO_BOX_FONT_SIZE)
        
        # Récup icon ampoule pour les boites info
        self.bulb_icon = pygame.image.load(BULB_ICON_PATH).convert_alpha()
        # Redimensionnement de l'icon
        self.bulb_icon = pygame.transform.scale(self.bulb_icon, (30, 30))
        
        # Chargement des textes des boites d'infos depuis le fichier JSON
        self.info_box_texts = get_dialogues("info_boxes") or {}

        #self.tech_tree = self.game.data_manager.tech_tree.session_data

    def update(self, spaceship):
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

        # Update boites d'info
        self.update_info_boxes()

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

    def clear_dialogues(self):
        """Efface tous les dialogues et réinitialise les attributs liés."""
        self.dialogues = []
        self.current_dialogue_index = 0
        self.show_dialogues = False

    def add_info_box(self, key_or_text, duration=None):
        """
        Ajoute une boîte d'information à afficher.
        
        :param key_or_text: Clé du texte dans info_box_texts ou texte direct à afficher
        :param duration: Durée d'affichage en secondes (None = valeur par défaut)
        """
        # Si duration est None : utilise durée par défaut
        if duration is None:
            duration = INFO_BOX_DISPLAY_DURATION
        
        # Récup texte à partir de la clé si présente dans dico
        text = self.info_box_texts.get(key_or_text, key_or_text)
        
        # Création dico pour stocker infos des boites d'infos
        info_box = {
            "text": text,
            # Heure création (pour calculer temps d'affichage)
            "creation_time": time.time(),
            # Durée d'affichage
            "duration": duration,
            # Transparence
            "opacity": 180,
            "rendered_lines": [],
        }
        
        # Découper texte en lignes pour retours à la lignes
        # Liste vide pour stocker les lignes de texte
        lines = []
        ## Découper le texte en mots
        words = text.split()
        # Première ligne de texte (avec premier mot)
        current_line = words[0]
        
        # Itère sur les mots restants de la ligne
        for word in words[1:]:
            # Test si le prochain mot rentre encore sur la ligne
            test_line = current_line + " " + word
            # Récup largeur ligne testée
            test_width, _ = self.info_box_font.size(test_line)
            
            # Si largeur ligne testée inférieure à largeur max
            if test_width <= INFO_BOX_MAX_WIDTH:
                # Ajoute le mot à la ligne courante
                current_line = test_line
            # Sinon ajoute la ligne courante à la liste et vérif la ligne suivante
            else:
                lines.append(current_line)
                current_line = word
        
        # Ajouter dernière ligne
        if current_line:
            lines.append(current_line)
        
        # Render chaque ligne de texte
        for line in lines:
            rendered_line = self.info_box_font.render(line, True, (255, 255, 255))
            info_box["rendered_lines"].append(rendered_line)
        
        # Ajouter la boite d'info à la liste
        self.info_boxes.append(info_box)

    def update_info_boxes(self):
        """
        Met à jour les boîtes d'information (durée, animations, etc.)
        et supprime celles qui ont dépassé leur durée d'affichage.
        """
        current_time = time.time()
        updated_boxes = []
        
        for box in self.info_boxes:
            # Calculer le temps écoulé depuis la création
            elapsed = current_time - box["creation_time"]
            
            # Vérifier si la boîte d'info doit être conservée
            if elapsed < box["duration"]:
                # Animation transparence
                if elapsed < 0.5:
                    # Fade-in 0.5sec
                    box["opacity"] = int(230 * (elapsed / 0.5))
                elif elapsed > box["duration"] - 0.5:
                    # Fade-out 0.5sec
                    box["opacity"] = int(230 * ((box["duration"] - elapsed) / 0.5))
                else:
                    box["opacity"] = 230
                
                # Conserver cette boîte
                updated_boxes.append(box)
        
        # Update liste des boites d'info
        self.info_boxes = updated_boxes

    def draw_info_boxes(self, surface):
        """
        Dessine les boîtes d'information actives sur l'écran.
        """
        if not self.info_boxes:
            return
        
        # Position départ pour les boîtes d'info
        start_x, start_y = 10, 40
        # Espace entre bord et contenu
        padding = 10
        # Espace entre lignes
        line_spacing = 5
        # Espace entre boites (si plusieurs)
        box_spacing = 10
        # Coordonnée y première boite
        current_y = start_y
        
        #Itérer sur chaque boîte d'info
        for box in self.info_boxes:
            # Récup dimensions des lignes affichées
            line_heights = [line.get_height() for line in box["rendered_lines"]]
            max_width = max([line.get_width() for line in box["rendered_lines"]], default=0)
            
            # Calculer dimensions icon ampoule
            icon_width = self.bulb_icon.get_width()
            # Calculer dimensions boite info (avec marge sur les côtés)
            box_width = max(icon_width, max_width) + 2 * padding + 40
            box_height = sum(line_heights) + (len(line_heights) - 1) * line_spacing + 2 * padding
            
            # Créer surface boite
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            
            # Remplir avec une couleur semi-transparente
            box_surface.fill((0, 0, 0, int(box["opacity"] * 0.8)))
            
            # Dessiner contour boite
            pygame.draw.rect(box_surface, (100, 100, 100, box["opacity"]), (0, 0, box_width, box_height), 1)
            
            # Dessiner icon ampoule
            icon_with_opacity = self.bulb_icon.copy()
            icon_with_opacity.set_alpha(box["opacity"])
            box_surface.blit(icon_with_opacity, (padding, padding))
            
            # Dessiner le texte ligne par ligne
            text_x = padding + icon_width + 5
            text_y = padding
            
            # Itère sur les lignes de texte
            for line in box["rendered_lines"]:
                # Dessine ligne
                box_surface.blit(line, (text_x, text_y))
                # Update coordonnée Y pour ligne suivante
                text_y += line.get_height() + line_spacing
            
            # Dessiner boite d'info sur l'écran
            surface.blit(box_surface, (start_x, current_y))
            
            # Update de la coordonnée Y pour la prochaine boite
            current_y += box_height + box_spacing

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
        """Dessine la liste des ressources de la planète atterrie sur le côté gauche, avec un fond."""
        if not self.landed_planet:
            # Repasse le rect à None si pas atterri (redécollé)
            self.collect_button_rect = None
            return

        # Définition des constantes

        # Position X de départ pour le contenu (marge à gauche)
        start_x = 20
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
        # Dessiner de la surface de fond sur l'écran principal - Position X ajustée
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
            else:
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
        button_color = (80, 80, 120)
        mouse_pos = pygame.mouse.get_pos()
        if self.collect_button_rect.collidepoint(mouse_pos):
            # Couleur plus claire au survol
            button_color = (100, 100, 150)

        # Dessiner le fond du bouton
        pygame.draw.rect(surface, button_color, self.collect_button_rect)
        # Dessiner une bordure autour du bouton
        pygame.draw.rect(surface, (200, 200, 200), self.collect_button_rect, 2)

        # Dessiner le texte du bouton
        button_text = "Récupérer les ressources"
        button_text_surf = self.resource_font.render(button_text, True, (255, 255, 255))
        button_text_rect = button_text_surf.get_rect(center=self.collect_button_rect.center)
        surface.blit(button_text_surf, button_text_rect)

    def draw_dialogues(self, surface):
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

    def draw_controls_info(self, surface):
        """Dessine les informations des contrôles de base en bas à droite,
           uniquement si aucun dialogue n'est affiché."""
        # Ne pas afficher les contrôles si un dialogue est en cours (pour le tuto)
        if self.show_dialogues:
            return

        # Variables pour mise en page
        # Marges autour du bloc de contrôles
        margin_right = 20
        # Marge en bas de l'écran
        margin_bottom = 20
        # Espace entre image et texte
        padding_horizontal = 8
        # Espace entre les lignes
        padding_vertical = 5
        # Largeur d'une image de touche (toutes les images ont la mm hauteur normalement)
        line_height = self.key_q_img.get_height()

        # Textes des contrôles
        labels = {
            "q": "Rotation Gauche",
            "d": "Rotation Droite",
            "space": "Moteur",
            "i": "Inventaire",
            "c": "Zone Assemblage",
            "m": "Ouvrir Map",
            "t": "Arbre Technologie",
            "esc": "Menu Pause"
        }

        # Rendu des surfaces de texte
        rendered_labels = {key: self.controls_font.render(text, True, (200, 200, 200)) for key, text in labels.items()}

        # Calcul de la largeur max pour le bloc de contrôles
        max_line_width = 0
        # Itère sur les touches (pour trouver largeur max)
        for key in ["q", "d", "space", "i", "c", "m", "t", "esc"]:
            key_img = getattr(self, f"key_{key}_img") # Récupère l'image dynamiquement
            line_width = key_img.get_width() + padding_horizontal + rendered_labels[key].get_width()
            max_line_width = max(max_line_width, line_width)

        # Récupère taille écran
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Position X de départ pour les images (alignées à gauche du bloc)
        start_x_img = screen_width - margin_right - max_line_width

        # Position Y de départ (pour dernière ligne)
        current_y = screen_height - margin_bottom - line_height

        # Dessin des lignes (bas en haut)

        # Ligne 8: Echap
        # récupère l'image de la touche Echap
        key_img = self.key_esc_img
        # récupère le texte de la touche Echap (depuis dico)
        label = rendered_labels["esc"]
        # Position X du texte = Position X de l'image + largeur de l'image + espace horizontal
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        # Dessine l'image de la touche Echap et le texte à l'écran
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        # Remonter la position Y pour la prochaine ligne
        current_y -= (line_height + padding_vertical)

        # Ligne 7: T (tjr pareil)
        key_img = self.key_t_img
        label = rendered_labels["t"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        current_y -= (line_height + padding_vertical)

        # Ligne 6: M
        key_img = self.key_m_img
        label = rendered_labels["m"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        current_y -= (line_height + padding_vertical)

        # Ligne 5: C
        key_img = self.key_c_img
        label = rendered_labels["c"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        current_y -= (line_height + padding_vertical)

        # Ligne 4: I
        key_img = self.key_i_img
        label = rendered_labels["i"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        current_y -= (line_height + padding_vertical)

        # Ligne 3: Espace
        key_img = self.key_space_img
        label = rendered_labels["space"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        current_y -= (line_height + padding_vertical)

        # Ligne 2: D
        key_img = self.key_d_img
        label = rendered_labels["d"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        current_y -= (line_height + padding_vertical)

        # Ligne 1: Q
        key_img = self.key_q_img
        label = rendered_labels["q"]
        pos_x_text = start_x_img + key_img.get_width() + padding_horizontal
        surface.blit(key_img, (start_x_img, current_y))
        surface.blit(label, (pos_x_text, current_y + (line_height - label.get_height()) // 2))
        # Pas besoin de décrémenter current_y car dernière ligne (+ haute)

    def draw_game_timer(self, surface, timer_value):
        """
        Dessine le timer du jeu en bas au centre de l'écran.
        :param surface: La surface sur laquelle dessiner.
        :param timer_value: Le temps restant en secondes.
        """
        # Formater le temps en MM:SS
        minutes = int(timer_value // 60)
        seconds = int(timer_value % 60)
        # Création texte timer
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        # Render le texte
        timer_surface = self.font.render(timer_text, True, (255, 255, 255))
        
        # Positionner le texte en bas au centre
        timer_rect = timer_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        
        surface.blit(timer_surface, timer_rect)

    def draw_install_colony_button(self, surface, game):
        """
        Dessine le bouton "Installer la colonie" si les conditions sont remplies.
        Conditions : Vaisseau atterri sur une planète habitable ET le joueur possède "colony_kit".
        """
        # Réinitialiser le rect du bouton par défaut
        self.install_colony_button_rect = None

        if game.spaceship and game.spaceship.is_landed and game.spaceship.landed_planet:
            # Vérifier si la planète est habitable et si le joueur a un colony_kit
            if game.spaceship.landed_planet.planet_type == "habitable" and game.data_manager.inventory.has_item("colony_kit", 1):
                # Définition des dimensions et position du bouton
                button_width = WINDOW_WIDTH * 0.4
                button_height = 55
                # Centrer horizontalement
                button_x = (WINDOW_WIDTH - button_width) // 2
                # Marge 125 px en bas
                button_y = WINDOW_HEIGHT - button_height - 125

                self.install_colony_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                # Couleur bouton
                button_color = (0, 100, 0)
                mouse_pos = pygame.mouse.get_pos()
                # Plus clair si survolé
                if self.install_colony_button_rect.collidepoint(mouse_pos):
                    button_color = (0, 150, 0)

                # Dessiner fond bouton
                pygame.draw.rect(surface, button_color, self.install_colony_button_rect, border_radius=10)
                # Dessiner bordure
                pygame.draw.rect(surface, (200, 255, 200), self.install_colony_button_rect, 2, border_radius=10)

                # Texte du bouton
                button_text = "Installer la colonie sur la planète"
                # Utiliser police HUD
                button_text_surf = self.font.render(button_text, True, (255, 255, 255))
                button_text_rect = button_text_surf.get_rect(center=self.install_colony_button_rect.center)
                surface.blit(button_text_surf, button_text_rect)

    def draw(self, surface, camera, world_surface, world_surface_wiouth_stars, persistent_game_timer_value, tech_tree, game):
        """
        Dessine l'HUD.
        """

        # Récupère les coordonnées de la grille
        # Affiche la grille si DEBUG_MODE = True
        coord = grille(DEBUG_MODE)

        # Création des textes à afficher
        position_text = f"Position: x: {self.position[0]:.2f}, y: {self.position[1]:.2f}"
        velocity_text = f"Vitesse: {self.velocity:.2f}"
        forces_text = f"resultant force: {self.resultant_force:.2f}"
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
        draw_buttons("crafting", (30, 30))


        if tech_tree["tech_tree"]["nitrogen"]["tiers"]["tier_4"]["unlocked"]:
            SPACESHIP_MAX_NITROGEN = 320
        elif tech_tree["tech_tree"]["nitrogen"]["tiers"]["tier_3"]["unlocked"]:
            SPACESHIP_MAX_NITROGEN = 160
        elif tech_tree["tech_tree"]["nitrogen"]["tiers"]["tier_2"]["unlocked"]:
            SPACESHIP_MAX_NITROGEN = 80
        elif tech_tree["tech_tree"]["nitrogen"]["tiers"]["tier_1"]["unlocked"]:
            SPACESHIP_MAX_NITROGEN = 40
        elif tech_tree["tech_tree"]["nitrogen"]["tiers"]["tier_0"]["unlocked"]:
            SPACESHIP_MAX_NITROGEN = 20

        
        if tech_tree["tech_tree"]["propellant"]["tiers"]["tier_4"]["unlocked"]:
            SPACESHIP_MAX_PROPELLANT = 1000
        elif tech_tree["tech_tree"]["propellant"]["tiers"]["tier_3"]["unlocked"]:
            SPACESHIP_MAX_PROPELLANT = 500
        elif tech_tree["tech_tree"]["propellant"]["tiers"]["tier_2"]["unlocked"]:
            SPACESHIP_MAX_PROPELLANT = 250
        elif tech_tree["tech_tree"]["propellant"]["tiers"]["tier_1"]["unlocked"]:
            SPACESHIP_MAX_PROPELLANT = 100
        elif tech_tree["tech_tree"]["propellant"]["tiers"]["tier_0"]["unlocked"]:
            SPACESHIP_MAX_PROPELLANT = 50

        
        nitrogen=float(left_nitrogen_text[9:])
        propellant=float(left_propellant_text[11:])


        if propellant==SPACESHIP_MAX_PROPELLANT:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant\propellant_max.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*90:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_9.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*80:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_8.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*70:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_7.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*60:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_6.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*50:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_5.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*40:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_4.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*30:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_3.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*20:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_2.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*10:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_1.png").convert_alpha()
        else:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_0.png").convert_alpha()

        coord_hud=hud_draw(38,31,50,35)
        screen.blit(propellant_image, coord_hud)

        
        if nitrogen==SPACESHIP_MAX_NITROGEN:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_max.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*90:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_9.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*80:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_8.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*70:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_7.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*60:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_6.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*50:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_5.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*40:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_4.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*30:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_3.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*20:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_2.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*10:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_1.png").convert_alpha()
        else:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_0.png").convert_alpha()

        coord_hud=hud_draw(38,33,50,35)
        screen.blit(nitrogen_image, coord_hud)

        propelent = left_propellant_text[11:] + "/" +str(SPACESHIP_MAX_PROPELLANT)
        draw_text(custom_size(33.5, 31.25), propelent)
        nitrogen = left_nitrogen_text[9:] +"/"+ str(SPACESHIP_MAX_NITROGEN)
        draw_text(custom_size(33.5, 33.25), nitrogen)
        position_x = position_text[9:17]
        draw_text(custom_size(13, 31), position_x)
        position_y = position_text[21:29]
        draw_text(custom_size(13, 31.75), position_y)
        draw_text(custom_size(13, 33), velocity_text)
        draw_text(custom_size(18, 31), forces_text)

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

        # Dessiner le bouton d'installation de la colonie si les conditions sont remplies
        self.draw_install_colony_button(surface, game)

        # Dessiner les boîtes d'information
        self.draw_info_boxes(surface)

        # Dessiner le dialogue actuel si nécessaire
        self.draw_dialogues(surface)

        # Dessiner les informations des touches de contrôles
        self.draw_controls_info(surface)

        # Dessiner le timer du jeu
        self.draw_game_timer(surface, persistent_game_timer_value)
