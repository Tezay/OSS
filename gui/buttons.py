import pygame
import math

from config import *


class Button():
    def __init__(self,coord,width,height,text,file, text_color=(255,255,255),text_size=24):
        self.x=coord[0]
        self.y=coord[1]
        self.width=width
        self.height=height
        self.button_rect = pygame.Rect(coord[0], coord[1], width, height)
        self.text=text
        self.file=file
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.Font(FONT_PATH, self.text_size)

    def draw(self):
        # Charger la texture du bouton
        texture = pygame.image.load(self.file)

        # Redimensionner la texture pour qu'elle soit de la même taille que le bouton
        texture = pygame.transform.scale(texture, (self.width, self.height))

        # Vérifier si la souris est sur l'image
        if texture.get_rect(topleft=(self.x, self.y)).collidepoint(pygame.mouse.get_pos()):
            # Charger la texture avec des contours blancs
            if self.file=="assets/button.png":
                texture = pygame.transform.scale(pygame.image.load("assets/button_highlighted.png"), (self.width, self.height))
                screen.blit(texture, (self.x, self.y))
            elif self.file=="assets\hud\settings.png":
                texture = pygame.transform.scale(pygame.image.load("assets\hud\settings.png"), (self.width+4, self.height+4))
                screen.blit(texture, (self.x-2, self.y-2))
            elif self.file=="assets\hud/tech_tree.png":
                texture = pygame.transform.scale(pygame.image.load("assets\hud/tech_tree_hoover.png"), (self.width+4, self.height+4))
                screen.blit(texture, (self.x-2, self.y-2))
            elif self.file=="assets\hud/inventory.png":
                texture = pygame.transform.scale(pygame.image.load("assets\hud/inventory_hoover.png"), (self.width, self.height))
                screen.blit(texture, (self.x, self.y))
        else:
            screen.blit(texture, (self.x, self.y))

        

        # Rendu du texte avec la police custom
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def click(self,mouse_x,mouse_y):
        # Vérifie si les coordonnées de la position de la souris sont comprisent dans les coordonnées du bouton
        if self.button_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False
        
    def colide(self,mouse_x,mouse_y):
        if self.button_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

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
        for j in range(0,WINDOW_HEIGHT,WINDOW_HEIGHT//35):
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



def custom_size(widht, height):
    square=grille(False)
    if type(widht)==int and type(height)==int:
        custom_widht=square[widht][height][1]    #x sur la grille    
        custom_height=square[widht][height][0]    #y sur la grille
    elif type(widht)==int and type(height)==float:
        custom_widht=square[int(widht)][int(height)][1]   #x sur la grille    
        custom_height=square[int(widht)][int(height)][0]+height%1*square[0][1][0]    #y sur la grille
    elif type(widht)==float and type(height)==int:
        custom_widht=square[int(widht)][int(height)][1]+widht%1*square[1][0][1]   #x sur la grille
        custom_height=square[int(widht)][int(height)][0]    #y sur la grille
    elif type(widht)==float and type(height)==float:
        custom_widht=square[int(widht)][int(height)][1]+widht%1*square[1][0][1]   #x sur la grille
        custom_height=square[int(widht)][int(height)][0]+height%1*square[0][1][0]    #y sur la grille
    return (custom_widht,custom_height)

def normal_size():
    return custom_size(12,4)


def hud_draw(x,y,x_fin,y_fin):
    coord_buttons=grille(False)
    pygame_x=coord_buttons[x][y][1]                 #extraction de la premiere coordoné (en x) via la grille de coordoné
    pygame_y=coord_buttons[x][y][0]                 #extraction de la deuxième coordoné (en y) via la grille de coordoné
    pygame_x_end=coord_buttons[x_fin][y][1]-pygame_x    #definition de la taille en x
    pygame_y_end=coord_buttons[x][y_fin][0]-pygame_y    #definition de la taille en y
    return(pygame_x,pygame_y,pygame_x_end,pygame_y_end)

def draw_size_buttons(name,x,y,size=normal_size(),txt=None,color=(255,255,255)):
    coord_buttons=grille(False)
    button=buttons[name]            #extraire le dictionaire associé au bouton voulue
    if type(x)==int and type(y)==int:
        x_coord=coord_buttons[x][y][1]    #x sur la grille    
        y_coord=coord_buttons[x][y][0]    #y sur la grille
    elif type(x)==int and type(y)==float:
        x_coord=coord_buttons[int(x)][int(y)][1]   #x sur la grille    
        y_coord=coord_buttons[int(x)][int(y)][0]+x%1*coord_buttons[0][1][0]    #y sur la grille
    elif type(x)==float and type(y)==int:
        x_coord=coord_buttons[int(x)][int(y)][1]+x%1*coord_buttons[1][0][1]   #x sur la grille
        y_coord=coord_buttons[int(x)][int(y)][0]    #y sur la grille
    widht=size[0]              #taillee du bouton
    height=size[1]         #hauteur du bouton
    if txt==None:
        text=button["text"]                             #texte
    else:
        text=txt
    file=button["file"]                             #image a dessiner
    if len(button)==6:
        text_size=button["text_size"]                     #taille du texte
    else:
        text_size=24
    return Button((x_coord,y_coord),widht,height,text,file,color,text_size).draw()



def draw_buttons(name,size=normal_size()):
    coord_buttons=grille(False)
    button=buttons[name]            #extraire le dictionaire associé au bouton voulue
    x=coord_buttons[button["x"]][button["y"]][1]    #x sur la grille    
    y=coord_buttons[button["x"]][button["y"]][0]    #y sur la grille
    widht=size[0]                                   #taillee du bouton
    height=size[1]                                  #hauteur du bouton
    color=button["color"]                           #couleur du texte
    text=button["text"]                             #texte
    file=button["file"]                             #image a dessiner
    if len(button)==6:
        text_size=button["text_size"]                     #taille du texte
    else:
        text_size=24

    return Button((x,y),widht,height,text,file,color,text_size).draw()


def click_button(name,mouse_pos,size=normal_size()):
    coord_buttons=grille(False)
    button=buttons[name]
    x=coord_buttons[button["x"]][button["y"]][1]
    y=coord_buttons[button["x"]][button["y"]][0]
    widht=size[0]
    height=size[1]
    color=button["color"]
    text=button["text"]
    file=button["file"]
    return Button((x,y),widht,height,color,text,file).click(mouse_pos[0],mouse_pos[1])

def colide_button(name,mouse_pos,size=normal_size()):
    coord_buttons=grille(False)
    button=buttons[name]
    x=coord_buttons[button["x"]][button["y"]][1]
    y=coord_buttons[button["x"]][button["y"]][0]
    widht=size[0]
    height=size[1]
    if x <= mouse_pos[0] <= x + widht and y <= mouse_pos[1] <= y + height:
        return True
    else:
        return False
    
#circle_click(self,button_center,button_radius,mouse_x,mouse_y)    
def colide_circle_button(radius,mouse_pos,coord):
    distance = math.sqrt((mouse_pos[0] - coord[0]) ** 2 + (mouse_pos[1] - coord[1]) ** 2)
    # Vérification si la souris est dans le cercle
    if distance <= radius:
        print("Bouton circulaire cliqué")
        return True
    else:
        return False
    """if x <= mouse_pos[0] <= x + widht and y <= mouse_pos[1] <= y + height:
        return True
    else:
        return False"""

def colide_image(mouse_pos,x,y,cell_size):
    if x <= mouse_pos[0] <= x + cell_size and y <= mouse_pos[1] <= y + cell_size:
        return True
    else:
        return False

    
def colide_draw_coord(txt,mouse,x,y,cell_size):
    if colide_image(mouse,x,y,cell_size):
        return overlay(txt,mouse)

def colide_draw(name,txt,mouse,size=normal_size()):
    if colide_button(name,mouse,size):
        return overlay(txt,mouse)


def position_button(name):
    coord_buttons=grille(False)
    button=buttons[name]
    x=coord_buttons[button["x"]][button["y"]][1]
    y=coord_buttons[button["x"]][button["y"]][0]
    return [x,y]



def overlay(txt, mouse):
    coord_buttons=grille(False)
    # Chemin de l'image source
    image_path = "assets/overlay_texture.png"
    original_image = pygame.image.load(image_path).convert_alpha()


    # Taille de l'image
    tech_button_size_widht =coord_buttons[16][0][1]    #x sur la grille
    tech_button_size_height = coord_buttons[0][9][0]   #y sur la grille
    # Recadrer et forcer le redimensionnement exact
    resized_image = pygame.transform.scale(original_image, (tech_button_size_widht, tech_button_size_height))

    # Ajouter transparence
    alpha = 240
    resized_image.set_alpha(alpha)

    # Initialisation police
    font = pygame.font.Font(FONT_PATH, 17)

    # Gestion du texte (multi-lignes si nécessaire)
    padding = 20
    max_text_width = tech_button_size_widht - 2 * padding
    words = txt.split(' ')
    lines = []
    line = []
    line_width = 0
    space_width = font.size(' ')[0]

    for word in words:
        word_width = font.size(word)[0]
        if word == "\n":  # Saut de ligne explicite
            lines.append(' '.join(line))
            line=[]
            line_width = word_width
        elif line_width + word_width + space_width > max_text_width or word== "\n":  # Nouvelle ligne nécessaire
            lines.append(' '.join(line))
            line = [word]
            line_width = word_width
        else:
            line.append(word)
            line_width += word_width + space_width

    if line:
        lines.append(' '.join(line))

    # Calculer la hauteur totale du texte
    line_height = font.get_linesize()
    total_text_height = len(lines) * line_height

    # Vérifier si le texte dépasse l'image (limitation simple)
    if total_text_height > tech_button_size_height:
        print("Attention : Le texte dépasse la zone de l'image !")
        return

    text_y = (tech_button_size_height - total_text_height) // 2  # Centrer verticalement
    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))  # Texte blanc
        text_x = padding  # Décalage constant depuis la gauche (marge gauche)
        resized_image.blit(text_surface, (text_x, text_y))
        text_y += line_height  # Avancer vers la ligne suivante


    # Afficher l'image redimensionnée avec texte sur l'écran
    screen.blit(resized_image, (mouse[0], mouse[1]))

def draw_text(coord, txt, font_size=12, color=(255, 255, 255)):
    x = coord[0]
    y = coord[1]
    font = pygame.font.Font(FONT_PATH, font_size)

    # Diviser le texte en lignes
    lines = txt.split('\n')

    # Rendre et dessiner chaque ligne de texte
    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += font.get_linesize()  # Déplacer la position y pour la ligne suivante 