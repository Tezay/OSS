import pygame
import math
from config import*


# Ca c'est ghetto, faut faire autrements
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Button():
    def __init__(self,x,y,width,height,color,text,dif_hoover,file,font="Arial",text_color=(255,255,255),text_size=8):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
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
        if self.x< mouse_x < self.x+self.width and self.y< mouse_y < self.y+self.height:
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


def tech_tree_button():
    return Button(WINDOW_WIDTH//8, WINDOW_HEIGHT//10, button_size_widht, button_size_height, (255, 255, 255), "Arbre technologique",30,"assets/button.png")

def test():
    return Button(WINDOW_WIDTH//8, WINDOW_HEIGHT//10, button_size_widht, button_size_height, (255, 255, 255), "Bouton test",30,"assets/button.png")

def resolution_screen_button():
    return Button(900,350,button_size_widht, button_size_height, (255, 255, 255), "Résolution",30,"assets/button.png")

def launch_button():
    return Button(350,460, button_size_widht, button_size_height, (255, 0, 0), "Lancer le jeu", 20, "assets/button.png")

def menu_settings_button():
    return Button(650,370, button_size_widht, button_size_height, (255, 0, 0), "Paramètres", 0, "assets/button.png")

def game_settings_button():
    return Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200, button_size_widht, button_size_height, (255, 0, 0), "Paramètres jeu", 30, "assets/button.png")

def quit_button():
    return Button(650,460, button_size_widht, button_size_height, (255, 0, 0), "Quitter", 20, "assets/button.png")

def return_button():
    return Button(735, 585, button_size_widht, button_size_height, (255, 255, 255), "Retour", 0, "assets/button.png")

def full_screen_button():
    return Button(250,130, button_size_widht, button_size_height, (255, 255, 255), "Plein ecran", 0, "assets/button.png")

def resolution_1280x720_button():
    return Button(250,200, button_size_widht, button_size_height, (255, 255, 255), "1280x720", 0, "assets/button.png")

def resolution_1920x1080_button():
    return Button(250,270, button_size_widht, button_size_height, (255, 255, 255), "1920x1080", 0, "assets/button.png")

def resolution_1920x1200_button():
    return Button(250,340, button_size_widht, button_size_height, (255, 255, 255), "1920x1200", 0, "assets/button.png")



