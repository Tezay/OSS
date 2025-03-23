import pygame
import math

from config import SPACESHIP_MAX_SPEED, WORLD_WIDTH, WORLD_HEIGHT,SPACESHIP_MAX_PROPELLANT, SPACESHIP_MAX_NITROGEN

class Spaceship:
    def __init__(self, x, y, vx, vy, width, height, image_path, mass=40, max_propellant=SPACESHIP_MAX_PROPELLANT, max_nitrogen=SPACESHIP_MAX_NITROGEN):
        """
        :param x: Position en x du vaisseau (coin supérieur gauche)
        :param y: Position en y du vaisseau (coin supérieur gauche)
        :param vx: Vitesse en x du vaisseau
        :param vy: Vitesse en y du vaisseau
        :param width: Largeur du vaisseau
        :param height: Hauteur du vaisseau
        :param image_path: Chemin vers l'image à utiliser comme texture
        :param max_propellant: Quantité maximale de propergol
        :param max_nitrogen: Quantité maximale de nitrogène
        """
        # Charger les deux versions de la texture (normale et powered)
        self.texture_normal = pygame.image.load(image_path).convert_alpha()
        self.texture_powered = pygame.image.load(image_path.replace(".png", "_powered.png")).convert_alpha()
        
        # Redimensionner les deux textures
        self.texture_normal = pygame.transform.scale(self.texture_normal, (width, height))
        self.texture_powered = pygame.transform.scale(self.texture_powered, (width, height))
        
        # État initial : texture normale
        self.original_image = self.texture_normal
        self.is_powered = False

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

        # Gestion des carburants
        self.max_propellant = max_propellant
        self.propellant = max_propellant
        self.max_nitrogen = max_nitrogen
        self.nitrogen = max_nitrogen

    # Méthode pour reset l'emplacement/la vitesse du vaisseau et la remmetre au point de spawn
    def reset(self):
        """Réinitialise la position, la vitesse et les carburants du vaisseau."""
        self.x = WORLD_WIDTH // 2
        self.y = WORLD_HEIGHT // 2
        self.vx = 0
        self.vy = -10
        self.angle = 0
        self.is_landed = False
        self.propellant = self.max_propellant
        self.nitrogen = self.max_nitrogen

    def recharge_fuels(self):
        """Recharge complètement le propellant et le nitrogen."""
        self.propellant = self.max_propellant
        self.nitrogen = self.max_nitrogen

    def consume_propellant(self, amount):
        """Consomme une certaine quantité de propellant."""
        if self.propellant > 0:
            # Consomme la quantité de propergol spécifiée
            self.propellant -= amount
            # S'assure que le propergol ne devient pas négatif
            self.propellant = max(self.propellant, 0)

    def consume_nitrogen(self, amount):
        """Consomme une certaine quantité de nitrogen."""
        if self.nitrogen > 0:
            # Consomme la quantité de nitrogène spécifiée
            self.nitrogen -= amount
            # S'assure que le nitrogène ne devient pas négatif
            self.nitrogen = max(self.nitrogen, 0)

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

    def set_powered_texture(self, powered):
        """Change la texture en fonction de l'état des propulseurs"""
        if self.is_powered != powered:
            self.is_powered = powered
            self.original_image = self.texture_powered if powered else self.texture_normal
            # Met à jour l'image avec la rotation actuelle
            self.update_image_angle()

    def draw(self, surface):
        """
        Dessine le vaisseau.
        """
        surface.blit(self.image, self.rect)