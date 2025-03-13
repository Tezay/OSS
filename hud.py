import pygame
import math
from buttons import *
from config import*


# Classe pour gérer l'interface dans le jeu
class Hud:
    def __init__(self):
        self.velocity = 0

    def update(self, vx, vy):
        self.velocity = math.sqrt(vx**2 + vy**2)

    def draw(self, surface):
        """
        Dessine l'HUD.
        """

        # Récupère les coordonnées de la grille
        # Affiche la grille si DEBUG_MODE = True
        coord = grille(DEBUG_MODE)

        # Test d'affichage de la vélocité du vaisseau
        font = pygame.font.Font(None, 24)
        velocity_text = f"Velocity: {self.velocity:.2f}"
        text = font.render(velocity_text, True, (255, 255, 255))
        surface.blit(text, (20, 20))


        #### Partie d'Edouard, structure et commentaires à revoir ####

        # la variable coord est une matrice contenant toutes les coordonées des carrées de la grille de 60 par 35.
        # les coordonées sont sous forme de tupple (indice 0 pour la coordoné en hauteur, et 1 pour la largeur).
        # pour la taille du hud, on prend un carré de la grille ou l'on veux que le hud finisse, et on y soustrait la coordoné de base, de meme pour la hauteur.
        
        #parametre de hud_draw:(carré en x, carré en y, carré de fin en x, carré de fin en y)

        # Dessin de la mini map
        coord_minimap=hud_draw(52,1,60,9)
        pygame.draw.rect(screen,(0,0,255),coord_minimap)          
        # Dessin de l'HUD
        coord_hud=hud_draw(10,30,50,35)
        pygame.draw.rect(screen,(255,0,0),coord_hud)


        draw_buttons("game_settings")
        draw_buttons("tech_tree")

        #pygame.display.flip()
