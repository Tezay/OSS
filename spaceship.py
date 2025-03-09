import pygame


class Spaceship:
    def __init__(self, x, y, width, height, image_path, speed):
        """
        :param x: Position en x du vaisseau (coin supérieur gauche)
        :param y: Position en y du vaisseau (coin supérieur gauche)
        :param width: Largeur du vaisseau
        :param height: Hauteur du vaisseau
        :param image_path: Chemin vers l'image à utiliser comme texture
        :param speed: Vitesse de déplacement du vaisseau
        """
        # Charge l'image et la redimensionne
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        # Récupère le rectangle associé à l'image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self, dx, dy):
        """
        Déplace le vaisseau selon un vecteur (dx, dy).
        Le déplacement effectif est multiplié par la vitesse.
        """
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        """
        Dessine le vaisseau sur la surface Pygame fournie.
        """
        surface.blit(self.image, self.rect)