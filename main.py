from idlelib.textview import view_text

import pygame
import math
import numpy

pygame.init()
screen = pygame.display.set_mode((1500, 700))
pygame.display.set_caption("jeu de la fusée")


couleur=(0,0,255)
position=[750,600]


class Fusée():
    def __init__(self,taille,hauteur,masse,vitesse_max,vitesse,position):
        self.taille = taille
        self.masse = masse
        self.vitesse_max = vitesse_max
        self.vitesse=vitesse
        self.hauteur = hauteur
        self.position=position


    def touche(self):
        if keys[pygame.K_SPACE]:
            print("ici")
            if self.vitesse<self.vitesse_max:
                self.vitesse+=1
            if self.vitesse==self.vitesse_max:
                self.vitesse=self.vitesse_max
        else:
            if self.vitesse!=0:
                self.vitesse-=1

    def deplacement(self):
        if self.vitesse>self.vitesse_max/2 and self.vitesse!=self.vitesse_max:
            self.position[1]+=1
        elif self.vitesse==self.vitesse_max:
            self.position[1]+=2








running=True

fusé=Fusée(5,10,20,100,0,position)


while running:
    screen.fill((0,0,0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if keys[pygame.K_SPACE]:
        print("ici")
        if fusé.vitesse == fusé.vitesse_max:
            fusé.vitesse = fusé.vitesse_max
        else:
            fusé.vitesse += 1

    else:
        if fusé.vitesse != 0:
            fusé.vitesse -= 1

    if fusé.vitesse<fusé.vitesse_max/2 and position[1]!=600:
        position[1]+=2

    if fusé.vitesse > fusé.vitesse_max / 2:
        position[1] -= fusé.vitesse*0.05


    pygame.draw.rect(screen, couleur, (fusé.position[0], fusé.position[1],fusé.taille, fusé.hauteur))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()