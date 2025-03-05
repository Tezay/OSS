import pygame
from .base_state import BaseState
from button import *

button_lancement = Button(largeur_ecran // 3, hauteur_ecran // 4, largeur_ecran // 4, 100, (255, 0, 0),
                          "Bienvenue dans OSS", 20, "lancement.png")


class MenuState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        # Exemple d'éléments à afficher
        self.title_font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        # On peut gérer des événements de souris / clavier ici si besoin
        pass

    def update(self, dt, actions):
        # Si l'action "start_game" (définie dans config.py) est True, on passe au GameState
        if actions.get("start_game"):
            from .game_state import GameState
            self.state_manager.set_state(GameState(self.state_manager))

        for event in pygame.event.get():
            pos = event.pos
            mouse_x, mouse_y = pos
            #print(mouse_x, mouse_y)
            if event.type== pygame.MOUSEBUTTONDOWN:
                print(mouse_x, mouse_y)
                if button_lancement.click(mouse_x,mouse_y):
                    from .game_state import GameState
                    self.state_manager.set_state(GameState(self.state_manager))


    def draw(self, screen):
        screen.fill((0, 0, 0))

        """title_surf = self.title_font.render("Menu Principal", True, (255, 255, 255))
        info_surf = self.info_font.render("Appuyez sur ENTER pour lancer le jeu", True, (200, 200, 200))"""
        button_lancement.draw()


        """screen.blit(title_surf, (100, 100))
        screen.blit(info_surf, (100, 200))"""
