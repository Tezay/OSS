import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, CAMERA_SPEED, DEBUG_MODE

class Camera:
    def __init__(self, world_width, world_height):
        # La zone initiale de la caméra correspond à la taille de la fenêtre
        self.camera_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.world_width = world_width
        self.world_height = world_height
        self.target = None

        # Gestion du zoom
        self.zoom = 1.0  # 1.0 : pas de zoom
        self.MIN_ZOOM = 0.2   # dézoom maximum (affiche plus de monde)
        self.MAX_ZOOM = 5.0   # zoom maximum (affiche moins de monde)

    def set_target(self, target):
        self.target = target

    def update(self):
        # Si un target est défini et qu'on n'est pas en mode debug, la caméra se centre sur le target
        if self.target and not DEBUG_MODE:
            x = self.target.rect.centerx - WINDOW_WIDTH // 2
            y = self.target.rect.centery - WINDOW_HEIGHT // 2
            self.camera_rect = pygame.Rect(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        elif DEBUG_MODE:
            # Déplacement manuel de la caméra avec les flèches
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.camera_rect.x -= CAMERA_SPEED
            if keys[pygame.K_RIGHT]:
                self.camera_rect.x += CAMERA_SPEED
            if keys[pygame.K_UP]:
                self.camera_rect.y -= CAMERA_SPEED
            if keys[pygame.K_DOWN]:
                self.camera_rect.y += CAMERA_SPEED

            # Gestion du zoom avec Z (zoomer) et X (dézoomer)
            if keys[pygame.K_z]:
                self.zoom += 0.01
            if keys[pygame.K_x]:
                self.zoom -= 0.01
            self.zoom = max(self.MIN_ZOOM, min(self.zoom, self.MAX_ZOOM))

        # Calcul du centre de la caméra (position actuelle)
        center_x = self.camera_rect.x + WINDOW_WIDTH // 2
        center_y = self.camera_rect.y + WINDOW_HEIGHT // 2

        # Calcul de la taille de la zone visible en fonction du facteur de zoom
        view_width = WINDOW_WIDTH / self.zoom
        view_height = WINDOW_HEIGHT / self.zoom

        # Détermination de la zone de vue (view_rect)
        self.view_rect = pygame.Rect(
            int(center_x - view_width // 2),
            int(center_y - view_height // 2),
            int(view_width),
            int(view_height)
        )

    def apply(self, entity):
        """
        Applique le décalage de la vue à un objet.
        """
        return entity.rect.move(-self.view_rect.x, -self.view_rect.y)
