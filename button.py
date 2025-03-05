import pygame
from config import*

largeur_ecran=WINDOW_WIDTH
hauteur_ecran=WINDOW_HEIGHT
pygame.init()
screen = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("interface")
font=pygame.font.Font(None,36)


class Button():
    def __init__(self,x,y,largeur,hauteur,couleur,texte,dif_hoover,fichier):
        self.x=x
        self.y=y
        self.largeur=largeur
        self.hauteur=hauteur
        self.couleur=couleur
        self.texte=texte
        self.dif_hoover=dif_hoover
        self.fichier=fichier


    def draw(self):
        pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.largeur, self.hauteur))
        texte_surface = font.render(self.texte, True, (0, 0, 0))
        texte_rect = texte_surface.get_rect(center=(self.x + self.largeur // 2, self.y + self.hauteur // 2))
        screen.blit(texte_surface, texte_rect)

    def click(self,mouse_x,mouse_y):
        print("clique accepté",self.x,self.x+self.largeur,self.y,self.y+self.hauteur)
        if self.x< mouse_x < self.x+self.largeur and self.y< mouse_y < self.y+self.hauteur:
            print("cliquer")
            #clique=False
            return True

    def close(self):
        Button(0, 0, 20, 20, (255, 255, 255), "X").draw()

    def cirle_click(self,button_center,button_radius,mouse_x,mouse_y):
        distance = math.sqrt((mouse_x - button_center[0]) ** 2 + (mouse_y - button_center[1]) ** 2)
        if distance <= button_radius:  # Si la souris est dans le cercle
            print("Bouton circulaire cliqué !")

    def normal_image(self,objet):
        image = pygame.image.load(self.fichier)
        image = pygame.transform.scale(image, (self.largeur, self.hauteur))
        button_rect = image.get_rect(center=(self.x + self.largeur // 2, self.y + self.hauteur // 2))
        if objet=="image":
            return image
        elif objet=="rect":
            return button_rect

    def hoover_image(self,objet):
        image = pygame.image.load(self.fichier)
        image = pygame.transform.scale(image, (self.largeur+self.dif_hoover,self.hauteur+self.dif_hoover ))
        button_rect = image.get_rect(center=(self.x+self.largeur // 2,self.y+self.hauteur // 2))
        if objet=="image":
            return image
        elif objet=="rect":
            return button_rect
        return