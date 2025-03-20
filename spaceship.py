import pygame
import math
from config import SPACESHIP_MAX_SPEED, WORLD_WIDTH, WORLD_HEIGHT

class Spaceship:
    def __init__(self, x, y, vx, vy, width, height, image_path, mass=1.0):
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
        """
        # Charger l'image d'origine du vaisseau (sans rotation)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (width, height))

        # Angle du vaisseau en degrés : 0 = vaisseau pointe vers le haut
        self.angle = 0.0

        # Stocker la version "rotationnée" actuelle de l'image
        self.image = self.original_image

        # Position
        self.x = float(x)
        self.y = float(y)
        # Vitesse
        self.vx = float(vx)
        self.vy = float(vy)
        # Masse
        self.mass = float(mass)

        # Forces cumulées (remises à zéro chaque frame)
        self.force_x = 0.0
        self.force_y = 0.0

        # Création du rect et centré sur (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Booléen pour stocker si le vaisseau est atterri ou non
        self.is_landed = False
        # Stock la planète sur laquelle le vaisseau est posé
        self.landed_planet = None

    # Méthode pour reset l'emplacement/la vitesse du vaisseau et la remmetre au point de spawn
    def reset(self):
        self.x = WORLD_WIDTH // 2
        self.y = WORLD_HEIGHT // 2
        self.vx = 0
        self.vy = -10
        self.angle = 0
        self.is_landed = False


    def add_force(self, fx, fy):
        """Ajoute une force (en Newton) au vaisseau."""
        self.force_x += fx
        self.force_y += fy

    def rotate(self, degrees):
        """
        Fait tourner l'angle du vaisseau (en degrés).
        """
        self.angle += degrees
        # S'assure que l'angle reste entre 0 et 360
        self.angle %= 360

    def update_physics(self, dt):
        """
        Met à jour la position et la vitesse du vaisseau en tenant compte
        de la somme des forces extérieures, puis remet cette somme à zéro.
        """

        # Si le vaisseau est atteri, ne pas faire varier sa vitesse
        if self.is_landed:
            self.vx = 0
            self.vy = 0
            
        else:
            # Calcul de l’accélération (F = m*a => a = F/m)
            ax = (self.force_x / self.mass)
            ay = (self.force_y / self.mass)

            # Mise à jour des vitesses
            self.vx += ax * dt
            self.vy += ay * dt

            # Limitation de la vitesse max
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > SPACESHIP_MAX_SPEED:
                # Normalisation de la vitesse
                scale = SPACESHIP_MAX_SPEED / speed
                self.vx *= scale
                self.vy *= scale

        # Mise à jour de la position
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Remise à zéro de la somme des forces pour la frame suivante
        self.force_x = 0.0
        self.force_y = 0.0

        # Mise à jour du rect pour affichage/collisions
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update_image_angle(self):
        """
        Met à jour l'image en fonction de l'angle courant.
        (appeler après avoir modifié self.angle)
        """
        # On pivote l’image autour de son centre.
        # Par défaut rotate() tourne dans sens antihoraire : -self.angle pour avoir angle=0 <=> vaisseau vers le haut
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        # Recalcul du rect pour que le centre
        #old_center = self.rect.center
        #self.rect = self.image.get_rect()
        #self.rect.center = old_center

    def draw(self, surface):
        """
        Dessine le vaisseau.
        """
        surface.blit(self.image, self.rect)