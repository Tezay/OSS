import pygame


class Spaceship:
    def __init__(self, x, y, vx, vy, ax, ay, width, height, image_path, rotation):
        """
        :param x: Position en x du vaisseau (coin supérieur gauche)
        :param y: Position en y du vaisseau (coin supérieur gauche)
        :param vx: Vitesse en x du vaisseau
        :param vy: Vitesse en y du vaisseau
        :param ax: Accélération en x du vaisseau
        :param ay: Accélération en y du vaisseau
        :param width: Largeur du vaisseau
        :param height: Hauteur du vaisseau
        :param image_path: Chemin vers l'image à utiliser comme texture
        :param rotation: Rotation du vaisseau
        """
        # Charge l'image et la redimensionne
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

        # Stock la position sous forme de float
        self.x = float(x)
        self.y = float(y)

        # On stocke la vitesse
        self.vx = float(vx)
        self.vy = float(vy)

        # On stocke l'accélération
        self.ax = float(ax)
        self.ay = float(ay)

        # Création d'un rect pour gérer la détection de collisions ou le rendu
        # Note : pas utilisé comme source de vérité sur la position (c'est x,y qui priment)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Facteur de friction (décélération naturelle)
        # Mettre friction=1.0 pour aucune friction
        self.friction = 0.98

    def accelerate(self, ax, ay):
        """
        Modifie l'accélération courante du vaisseau.
        ax, ay : composantes d'accélération (en pixels/s²).
        """
        self.ax = ax
        self.ay = ay

    def update(self, dt):
        """
        Mises à jour de la vitesse et de la position en fonction de l'accélération.
        dt : temps écoulé depuis la dernière frame (secondes).
        """
        # Mise à jour la vitesse en tenant compte de l'accélération
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Application de la friction
        self.vx *= self.friction
        self.vy *= self.friction

        # Mise à jour la position
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Mise à jour le rect pour le dessin / collisions
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        """
        Dessine le vaisseau sur la surface Pygame fournie.
        """
        surface.blit(self.image, self.rect)