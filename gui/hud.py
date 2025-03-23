import pygame
import math

from gui.buttons import *
from config import *


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

        # Police de caractères pour le texte de l'HUD
        self.font = custom_font
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

    def update(self, x, y, vx, vy, propellant, nitrogen):
        # Position du vaisseau
        self.position = (x, y)
        # Calcul de la vélocité du vaisseau
        self.velocity = math.sqrt(vx**2 + vy**2)
        # Calcul de la force résultante
        self.resultant_force = math.sqrt(self.fx_indicator**2 + self.fy_indicator**2)
        # Calcul de l'angle de la force résultante
        self.resultant_angle = math.degrees(math.atan2(self.fy_indicator, self.fx_indicator))
        # Mise à jour des carburants restants
        self.left_propellant = propellant
        self.left_nitrogen = nitrogen

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

    def draw(self, surface, camera, world_surface):
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
        left_propellant_text = f"Propellant: {self.left_propellant:.2f}"
        left_nitrogen_text = f"Nitrogen: {self.left_nitrogen:.2f}"

        # Création des surfaces de texte
        position_surface = self.font.render(position_text, True, (255, 255, 255))
        velocity_surface = self.font.render(velocity_text, True, (255, 255, 255))
        forces_surface = self.font.render(forces_text, True, (255, 255, 255))
        left_propellant_surface = self.font.render(left_propellant_text, True, (255, 255, 255))
        left_nitrogen_surface = self.font.render(left_nitrogen_text, True, (255, 255, 255))

        # Affichage des textes à l'écran
        surface.blit(position_surface, (20, 20))
        surface.blit(velocity_surface, (20, 50))
        surface.blit(forces_surface, (20, 80))
        surface.blit(left_propellant_surface, (20, 110))
        surface.blit(left_nitrogen_surface, (20, 140))

        
        # Dessin de l'HUD
        coord_hud=hud_draw(10,30,50,35)
        pygame.draw.rect(screen,(255,0,0),coord_hud)

        # Dessin de la mini-map
        self.draw_minimap(surface, camera, world_surface)

        # Dessiner la flèche directionnelle de la force résultante
        arrow_x = 20
        arrow_y = 170
        # Rotation de la flèche pour pointer dans la direction de la force résultante (+270 pour l'angle initial de la flèche)
        rotated_arrow = pygame.transform.rotate(self.arrow_texture, -self.resultant_angle + 270)
        arrow_rect = rotated_arrow.get_rect(center=(arrow_x + self.arrow_texture.get_width() // 2, arrow_y + self.arrow_texture.get_height() // 2))
        surface.blit(rotated_arrow, arrow_rect.topleft)

        draw_buttons("game_settings")
        draw_buttons("tech_tree")
