from idlelib.textview import view_text

import pygame
import math




keys = pygame.key.get_pressed()

class fusée():
    def __init__(self,taille,masse,vitesse_max,vitesse):
        self.taille = taille
        self.masse = masse
        self.vitesse_max = vitesse_max
        self.vitesse=vitesse





    def dessiner(self):