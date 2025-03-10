import pygame
import math
from config import*
import time


# Ca c'est ghetto, faut faire autrements
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Button():
    def __init__(self,coord,width,height,color,text,dif_hoover,file,font="Arial",text_color=(255,255,255),text_size=8):
        self.x=coord[0]
        self.y=coord[1]
        self.width=width
        self.height=height
        self.button_rect = pygame.Rect(coord[0], coord[1], width, height)
        self.color=color
        self.text=text
        self.dif_hoover=dif_hoover
        self.file=file
        self.font = font
        self.text_color = text_color
        self.text_size = text_size

    def draw(self):
        # Charger la texture originale
        texture = pygame.image.load(self.file)

        # Redimensionner la texture pour qu'elle soit de la même taille que le bouton
        texture = pygame.transform.scale(texture, (self.width, self.height))

        # Vérifier si la souris est sur l'image
        if texture.get_rect(topleft=(self.x, self.y)).collidepoint(pygame.mouse.get_pos()):
            # Charger la texture avec des contours blancs
            texture = pygame.transform.scale(pygame.image.load("assets/button_highlighted.png"), (self.width, self.height))
        else:
            # Charger la texture originale
            texture = pygame.transform.scale(texture, (self.width, self.height))

        # Blitter la texture sur l'écran
        screen.blit(texture, (self.x, self.y))

        # Écrire le texte
        font = pygame.font.SysFont("Arial", 24)  # Police de caractères par défaut
        text = font.render(self.text, True, self.text_color)  # Texte à afficher

        # Calculer la position du texte pour qu'il soit centré sur le bouton
        text_rect = text.get_rect()
        text_rect.centerx = self.x + self.width // 2
        text_rect.centery = self.y + self.height // 2

        # Dessiner le texte sur l'écran
        screen.blit(text, text_rect)

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


"""
    def normal_picture(self,objet):
        picture = pygame.image.load(self.file)
        picture = pygame.transform.scale(picture, (self.width, self.height))
        button_rect = picture.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        if objet=="picture":
            return picture
        elif objet=="rect":
            return button_rect

    def hoover_picture(self,objet):
        picture = pygame.image.load(self.file)
        picture = pygame.transform.scale(picture, (self.width+self.dif_hoover,self.height+self.dif_hoover ))
        button_rect = picture.get_rect(center=(self.x+self.width // 2,self.y+self.height // 2))
        if objet=="picture":
            return picture
        elif objet=="rect":
            return button_rect
        return
"""


# Sert plus à rien ??
def style_image(name):
    if name().normal_picture("rect").collidepoint(pygame.mouse.get_pos()):
        return name().draw()
    else:
        return screen.blit(name().normal_picture("picture"), name().normal_picture("rect"))


"""
def launch_button():
    return Button(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 4, WINDOW_WIDTH // 4, WINDOW_WIDTH//4, (255, 0, 0),"Bienvenue dans OSS", 20, "assets/button.png")
            #POUR CHANGER LA POSITION: CHANGER LA 1 ET 2,           POUR LA TAILLE :3 ET 4

def menu_settings_button():
    return Button(WINDOW_WIDTH // 1.5, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 15, WINDOW_WIDTH//15, (255, 0, 0),"parametre", 0, "assets/button.png")

def game_settings_button():
    return Button(WINDOW_WIDTH // 1.5, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 15, WINDOW_WIDTH//15, (255, 0, 0),"parametre", 30, "assets/button.png")

def quit_button():
    return Button(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 8, WINDOW_WIDTH // 4, WINDOW_WIDTH//4, (255, 0, 0),"Bienvenue dans OSS", 20, "assets/button.png")

def return_button():
    return Button(WINDOW_WIDTH-20, 0, 20, 20, (255, 255, 255), "retour arriere",0,"assets/button.png")
"""


########################
# Toutes les fonctions relatives aux boutons du jeu
# Return à chaque fois un objet de la classe Button (avec les paramètres dédiés)
# Pour afficher un bouton, utiliser .draw() sur un l'appel
########################

# Grille pour visualiser la position des boutons (mode debug)
def grille():
    matrice_coord=[]
    mat=[]
    pygame.init()
    info = pygame.display.Info()
    WINDOW_WIDTH=info.current_w
    WINDOW_HEIGHT=info.current_h
    for i in range(0,WINDOW_WIDTH,WINDOW_WIDTH//60):
        for j in range(0,WINDOW_HEIGHT,WINDOW_HEIGHT//36):
            pygame.draw.rect(screen,(255,0,0),(i,j,WINDOW_WIDTH//30,WINDOW_WIDTH//30),1)
            mat.append((j,i))
        matrice_coord.append(mat)
        mat=[]
    return matrice_coord

coord_boutons=grille()
    

def tech_tree_button():
    return Button(coord_boutons[30][15], button_size_widht, button_size_height, (255, 255, 255), "Arbre technologique",30,"assets/button.png")

def test():
    return Button(coord_boutons[30][18], button_size_widht, button_size_height, (255, 255, 255), "Bouton test",30,"assets/button.png")

def resolution_screen_button():
    return Button(coord_boutons[20][20],button_size_widht, button_size_height, (255, 255, 255), "Résolution",30,"assets/button.png")

def launch_button():
    return Button(coord_boutons[10][2], button_size_widht, button_size_height, (255, 0, 0), "Lancer le jeu", 20, "assets/button.png")

def menu_settings_button():
    return Button(coord_boutons[20][2], button_size_widht, button_size_height, (255, 0, 0), "Paramètres", 0, "assets/button.png")

def game_settings_button():
    return Button(coord_boutons[3][5], button_size_widht, button_size_height, (255, 0, 0), "Paramètres jeu", 30, "assets/button.png")

def quit_button():
    return Button(coord_boutons[30][2],button_size_widht, button_size_height, (255, 0, 0), "Quitter", 20, "assets/button.png")

def return_button():
    return Button(coord_boutons[25][10], button_size_widht, button_size_height, (255, 255, 255), "Retour", 0, "assets/button.png")

def full_screen_button():
    return Button(coord_boutons[10][25], button_size_widht, button_size_height, (255, 255, 255), "Plein ecran", 0, "assets/button.png")

def resolution_1280x720_button():
    return Button(coord_boutons[15][25], button_size_widht, button_size_height, (255, 255, 255), "1280x720", 0, "assets/button.png")

def resolution_1920x1080_button():
    return Button(coord_boutons[20][25], button_size_widht, button_size_height, (255, 255, 255), "1920x1080", 0, "assets/button.png")

def resolution_1920x1200_button():
    return Button(coord_boutons[25][25], button_size_widht, button_size_height, (255, 255, 255), "1920x1200", 0, "assets/button.png")

def resolution_2560x1080_button():
    return Button(coord_boutons[30][25], button_size_widht, button_size_height, (255, 255, 255), "2560x1080", 0, "assets/button.png")

