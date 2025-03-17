import pygame
import math
from config import *


class Button():
    def __init__(self,coord,width,height,color,text,file, text_color=(255,255,255),text_size=24):
        self.x=coord[0]
        self.y=coord[1]
        self.width=width
        self.height=height
        self.button_rect = pygame.Rect(coord[0], coord[1], width, height)
        self.color=color
        self.text=text
        self.file=file
        self.text_color = text_color
        self.text_size = text_size
        self.font = custom_font

    def draw(self):
        # Charger la texture du bouton
        texture = pygame.image.load(self.file)

        # Redimensionner la texture pour qu'elle soit de la même taille que le bouton
        texture = pygame.transform.scale(texture, (self.width, self.height))

        # Vérifier si la souris est sur l'image
        if texture.get_rect(topleft=(self.x, self.y)).collidepoint(pygame.mouse.get_pos()):
            # Charger la texture avec des contours blancs
            texture = pygame.transform.scale(pygame.image.load("assets/button_highlighted.png"), (self.width, self.height))


        # Blitter la texture sur l'écran
        screen.blit(texture, (self.x, self.y))

        # Rendu du texte avec la police custom
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def click(self,mouse_x,mouse_y):
        # Vérifie si les coordonnées de la position de la souris sont comprisent dans les coordonnées du bouton
        if self.button_rect.collidepoint(mouse_x, mouse_y):
            return True

    def circle_click(self,button_center,button_radius,mouse_x,mouse_y):
        # Calcul de la distance entre la position de la souris et le centre du cercle
        distance = math.sqrt((mouse_x - button_center[0]) ** 2 + (mouse_y - button_center[1]) ** 2)
        # Vérification si la souris est dans le cercle
        if distance <= button_radius:
            print("Bouton circulaire cliqué")


########################
# Toutes les fonctions relatives aux boutons du jeu
# Return à chaque fois un objet de la classe Button (avec les paramètres dédiés)
# Pour afficher un bouton, utiliser .draw() sur un l'appel
########################

# Grille pour visualiser la position des boutons (mode debug)
#renvoi une matrice de 61x36 (longeur,hauteur) de tupple de coordoné(hauteur en indice0, largeur en indice 1)
#draw est un booléen qui dit si la grille sera dessiner a l'ecran ou non
def grille(draw):
    matrice_coord=[]
    mat=[]
    pygame.init()
    info = pygame.display.Info()
    #prend la taille actuel de l'ecran
    WINDOW_WIDTH=info.current_w
    WINDOW_HEIGHT=info.current_h
    compt_x=0
    compt_y=0
    font = pygame.font.Font(None, 24)
    #divise l'ecran en carré (60x36)
    for i in range(0,WINDOW_WIDTH,WINDOW_WIDTH//60):
        for j in range(0,WINDOW_HEIGHT,WINDOW_HEIGHT//36):
            #si le parametre de la fonction est True, on dessine la grille
            if draw==True:
                pygame.draw.rect(screen,(64,64,64,128),(i,j,WINDOW_WIDTH//30,WINDOW_WIDTH//30),1)
                txt_y=font.render(str(compt_y), True, (255, 255, 255))
                screen.blit(txt_y, (i, j))
            mat.append((j,i))
            #arreter le compteur de ligne a 35
            if compt_y==35 or compt_y=="":
                compt_y=""
            else:
                compt_y+=1
                #dessiner les numero
        if draw==True:
            txt_x=font.render(str(compt_x), True, (255, 255, 255))
            screen.blit(txt_x, (i, j))
        matrice_coord.append(mat)
        mat=[]
        compt_x+=1
    return matrice_coord



def hud_draw(x,y,x_fin,y_fin):
    coord_buttons=grille(False)
    pygame_x=coord_buttons[x][y][1]                 #extraction de la premiere coordoné (en x) via la grille de coordoné
    pygame_y=coord_buttons[x][y][0]                 #extraction de la deuxième coordoné (en y) via la grille de coordoné
    pygame_x_end=coord_buttons[x_fin][y][1]-pygame_x    #definition de la taille en x
    pygame_y_end=coord_buttons[x][y_fin][0]-pygame_y    #definition de la taille en y
    return(pygame_x,pygame_y,pygame_x_end,pygame_y_end)



def draw_buttons(name):
    coord_buttons=grille(False)
    button=buttons[name]            #extraire le dictionaire associé au bouton voulue
    x=coord_buttons[button["y"]][button["x"]][0]    #x sur la grille    
    y=coord_buttons[button["y"]][button["x"]][1]    #y sur la grille
    widht=button["button_size_widht"]               #taillee du bouton
    height=button["button_size_height"]             #hauteur du bouton
    color=button["color"]                           #couleur du texte
    text=button["text"]                             #texte
    file=button["file"]                             #image a dessiner
    return Button((x,y),widht,height,color,text,file).draw()


def click_button(name,mouse_pos):
    coord_buttons=grille(False)
    button=buttons[name]
    x=coord_buttons[button["y"]][button["x"]][0]
    y=coord_buttons[button["y"]][button["x"]][1]
    widht=button["button_size_widht"]
    height=button["button_size_height"]
    color=button["color"]
    text=button["text"]
    file=button["file"]
    return Button((x,y),widht,height,color,text,file).click(mouse_pos[0],mouse_pos[1])