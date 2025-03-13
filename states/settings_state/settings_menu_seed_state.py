import pygame
from buttons import*
from ..base_state import BaseState
from config import*
import config


coord=grille(False)



# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant

class MenuSettingsSeedState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager      
        self.active=False
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        self.txt=""
        #la variable coord est une matrice contenant toutes les coordonées des carrées de la grille de 60 par 35.
        # les coordonées sont sous forme de tupple (indice 0 pour la coordoné en hauteur, et 1 pour la largeur).
        self.input_box = pygame.Rect(coord[6][6][0], coord[6][6][1], 600, 50)                  
    def handle_event(self, event,pos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            from .settings_menu_state import MenuSettingsState
            self.state_manager.set_state(MenuSettingsState(self.state_manager))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(pos):
                self.active = not self.active  # Basculer l'état actif
            else:
                self.active = False
        
        # Gestion de l'entrée de texte

        if self.active:  # Si la zone de texte est active
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Validé
                    if self.text.isdigit():
                        if 0<=int(self.text)<=999999999:
                            #changer custom seed du module config afin de le reutiliser dans game pour prendre la seed rentrée par l'uttilisateur
                            config.custom_seed=int(self.text)
                            self.txt="seed: "+str(config.custom_seed)
                        else:
                            self.txt="seed trop longue"
                            self.text=""
                    else:
                        self.txt="seed invalide"
                        self.text=""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Supprimer le dernier caractère
                else:
                    self.text += event.unicode  # Ajouter le caractère saisi

    def update(self, dt, actions, pos, mouse_clicked):
        
        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos


        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("return",pos):
                from .settings_menu_state import MenuSettingsState
                # Passe l'état courant à menu_state
                self.state_manager.set_state(MenuSettingsState(self.state_manager))
            



    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        color = (255, 0, 0) if self.active else (200, 200, 200)
        pygame.draw.rect(screen, color, self.input_box, 2)  # Dessiner la zone de texte

        # Rendre le texte
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        

        text_surf = self.font.render(self.txt, True, (255, 255, 255))
        screen.blit(text_surf,(coord[10][6][0], coord[10][6][1]))

       
        # Dessin des boutons relatifs à l'état settings_menu_state (avec la méthode .draw() de la classe Button)

        draw_buttons("return")


