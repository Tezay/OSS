import pygame
import math
from config import*



pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("interface")
font=pygame.font.Font(None,36)


class Button():
    def __init__(self,x,y,width,height,color,text,dif_hoover,file):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.text=text
        self.dif_hoover=dif_hoover
        self.file=file


    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def click(self,mouse_x,mouse_y):
        #print("clique accepté",self.x,self.x+self.width,self.y,self.y+self.height)
        if self.x< mouse_x < self.x+self.width and self.y< mouse_y < self.y+self.height:
            #print("cliquer")
            #clique=False
            return True


    def cirle_click(self,button_center,button_radius,mouse_x,mouse_y):
        distance = math.sqrt((mouse_x - button_center[0]) ** 2 + (mouse_y - button_center[1]) ** 2)
        if distance <= button_radius:  # Si la souris est dans le cercle
            print("Bouton circulaire cliqué !")

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


def style_image(name):
    if name().normal_picture("rect").collidepoint(pygame.mouse.get_pos()):
        return screen.blit(name().hoover_picture("picture"), name().hoover_picture("rect"))
    else:
        return screen.blit(name().normal_picture("picture"), name().normal_picture("rect"))



def launch_button():
    return Button(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 4, WINDOW_WIDTH // 4, WINDOW_WIDTH//4, (255, 0, 0),"Bienvenue dans OSS", 20, "assets/lounch_game.png")
            #POUR CHANGER LA POSITION: CHANGER LA 1 ET 2,           POUR LA TAILLE :3 ET 4

def menu_settings_button():
    return Button(WINDOW_WIDTH // 1.5, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 15, WINDOW_WIDTH//15, (255, 0, 0),"", 30, "assets/settings.png")
def game_settings_button():
    return Button(WINDOW_WIDTH // 1.5, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 15, WINDOW_WIDTH//15, (255, 0, 0),"", 30, "assets/settings.png")
def quit_button():
    return Button(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 8, WINDOW_WIDTH // 4, WINDOW_WIDTH//4, (255, 0, 0),"Bienvenue dans OSS", 20, "assets/quit_game.png")

def return_button():
    return Button(WINDOW_WIDTH-20, 0, 20, 20, (255, 255, 255), "X",0,"assets/default_texture.png")
def tech_tree_button():
    return Button(WINDOW_WIDTH//8, WINDOW_HEIGHT//10, WINDOW_WIDTH // 4, WINDOW_WIDTH//4, (255, 255, 255), "",30,"assets/tech_tree.png")
def test():
    return Button(WINDOW_WIDTH//8, WINDOW_HEIGHT//10, WINDOW_WIDTH // 4, WINDOW_WIDTH//4, (255, 255, 255), "",30,"assets/default_texture.png")
def resolution_screen_button():
    text="résolution"
    button=Button(WINDOW_WIDTH//15, WINDOW_HEIGHT//10, WINDOW_WIDTH // 2, WINDOW_WIDTH//12, (255, 255, 255), "",30,"assets/button.png")
    #return button.blit(text, (10, 10))
    return button




