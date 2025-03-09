import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, CAMERA_SPEED, DEBUG_MODE

class Camera:
    def __init__(self, world_width, world_height):
        # La zone initiale de la caméra correspond au centre du monde, aux dimentions de la fenêtre
        world_center_width = world_width//2 - WINDOW_WIDTH//2
        world_center_height = world_height//2 - WINDOW_HEIGHT//2
        self.camera_rect = pygame.Rect(world_center_width, world_center_height, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.world_width = world_width
        self.world_height = world_height
        self.target = None

        # Gestion du zoom
        self.zoom = 1.0  # 1.0 : pas de zoom
        self.MIN_ZOOM = 0.2   # dézoom maximum (affiche plus de monde)
        self.MAX_ZOOM = 4.0   # zoom maximum (affiche moins de monde)

        # Initialisation de view_rect pour éviter l'erreur si draw() est appelé avant update()
        self.view_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    def set_target(self, target):
        self.target = target

    def update(self, actions):
        """
        On reçoit 'actions', un dict contenant l'état des touches.
        """
        # Si la caméra a une cible, et que le mode debug est désactivé, centrer la caméra sur la cible
        if self.target and not DEBUG_MODE:
            # Caméra centrée sur les coordonnées de la cible
            x = self.target.rect.x - WINDOW_WIDTH // 2
            y = self.target.rect.y - WINDOW_HEIGHT // 2
            self.camera_rect = pygame.Rect(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

            # Si le mode debug est activé, la caméra n'est pas centrée sur la cible
        elif DEBUG_MODE:
            # Déplacement manuel de la caméra
            if actions.get("camera_left"):
                self.camera_rect.x -= CAMERA_SPEED
            if actions.get("camera_right"):
                self.camera_rect.x += CAMERA_SPEED
            if actions.get("camera_up"):
                self.camera_rect.y -= CAMERA_SPEED
            if actions.get("camera_down"):
                self.camera_rect.y += CAMERA_SPEED

            # Gestion du zoom
            if actions.get("zoom_in"):
                self.zoom += 0.01
            if actions.get("zoom_out"):
                self.zoom -= 0.01
            # Update du zoom (avec gestion du zoom min et max)
            self.zoom = max(self.MIN_ZOOM, min(self.zoom, self.MAX_ZOOM))

        # Calcul du view_rect
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
