import pygame
import math


# Classe pour gérer l'interface dans le jeu
class Hud:
    def __init__(self):
        self.velocity = 0

    def update(self, vx, vy):
        self.velocity = math.sqrt(vx**2 + vy**2)

    def draw(self, surface):
        """
        Dessine l'HUD.
        """

        # Test d'affichage de la vélocité du vaisseau
        font = pygame.font.Font(None, 24)
        velocity_text = f"Velocity: {self.velocity:.2f}"
        text = font.render(velocity_text, True, (255, 255, 255))
        surface.blit(text, (20, 20))