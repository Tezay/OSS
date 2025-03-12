import pygame
import math
from buttons import *
from config import DEBUG_MODE


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
        
        # Dessin de la mini map
        pygame.draw.rect(screen,(0,0,255),(coord[52][1][1],coord[52][1][0],coord[60][0][1]-coord[52][1][1],coord[52][9][0]-coord[52][1][0]))          
        # Dessin de l'HUD
        pygame.draw.rect(screen,(0,255,0),(coord[10][30][1],coord[10][30][0],coord[50][30][1]-coord[10][30][1],coord[10][35][0]-coord[10][30][0]+20))    

        game_settings_button().draw()
        tech_tree_button().draw()

        #pygame.display.flip()
