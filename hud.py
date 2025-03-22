import pygame
import math
from buttons import *
from config import*


# Classe pour gérer l'interface dans le jeu
class Hud:
    def __init__(self):
        self.velocity = 0
        self.font = custom_font

    def update(self, vx, vy):
        self.velocity = math.sqrt(vx**2 + vy**2)

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
        minimap_surface = pygame.transform.scale(minimap_view, (minimap_width, minimap_height))

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

        # Test d'affichage de la vélocité du vaisseau
        velocity_text = f"Velocity: {self.velocity:.2f}"
        text = self.font.render(velocity_text, True, (255, 255, 255))
        surface.blit(text, (20, 20))

        #### Partie d'Edouard, structure et commentaires à revoir ####

        # la variable coord est une matrice contenant toutes les coordonées des carrées de la grille de 60 par 35.
        # les coordonées sont sous forme de tupple (indice 0 pour la coordoné en hauteur, et 1 pour la largeur).
        # pour la taille du hud, on prend un carré de la grille ou l'on veux que le hud finisse, et on y soustrait la coordoné de base, de meme pour la hauteur.
        
        #parametre de hud_draw:(carré en x, carré en y, carré de fin en x, carré de fin en y)



        
        # Dessin de l'HUD
        coord_hud=hud_draw(10,30,50,35)
        pygame.draw.rect(screen,(255,0,0),coord_hud)

        # Dessin de la mini-map
        self.draw_minimap(surface, camera, world_surface)

        draw_buttons("game_settings")
        draw_buttons("tech_tree")

        #pygame.display.flip()
