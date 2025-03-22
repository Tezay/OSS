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
        self.zoom = 1.8  # 1.0 : pas de zoom
        self.MIN_ZOOM = 0.05   # dézoom maximum (affiche plus de monde)
        self.MAX_ZOOM = 3.0   # zoom maximum (affiche moins de monde)

        # Initialisation des coordonnées de la caméra
        self.x = world_center_width
        self.y = world_center_height

        # Initialisation de view_rect pour éviter l'erreur si draw() est appelé avant update()
        self.view_rect = pygame.Rect(world_center_width, world_center_height, WINDOW_WIDTH, WINDOW_HEIGHT)

    def set_target(self, target):
        self.target = target

    def update(self, actions):
        """
        On reçoit 'actions', un dict contenant l'état des touches.
        """
        # Si la caméra a une cible, et que le mode debug est désactivé, centrer la caméra sur la cible
        if self.target and not DEBUG_MODE:
            # Caméra centrée sur les coordonnées de la cible
            self.x = self.target.rect.x - WINDOW_WIDTH // 2
            self.y = self.target.rect.y - WINDOW_HEIGHT // 2

            # Si le mode debug est activé, la caméra n'est pas centrée sur la cible
        elif DEBUG_MODE:
             # Déplacement proportionnel au zoom
            prop_camera_speed = CAMERA_SPEED / self.zoom

            # Déplacement manuel de la caméra
            if actions.get("camera_left"):
                self.x -=  prop_camera_speed
            if actions.get("camera_right"):
                self.x +=  prop_camera_speed
            if actions.get("camera_up"):
                self.y -=  prop_camera_speed
            if actions.get("camera_down"):
                self.y +=  prop_camera_speed

            # Gestion du zoom
            if actions.get("zoom_in"):
                self.zoom += 0.04
            if actions.get("zoom_out"):
                self.zoom -= 0.04
            # Update du zoom (avec gestion du zoom min et max)
            self.zoom = max(self.MIN_ZOOM, min(self.zoom, self.MAX_ZOOM))

        # Update du camera_rect à partir des nouvelles coordonnées de la caméra (dues déplacement)
        self.camera_rect = pygame.Rect(self.x, self.y, WINDOW_WIDTH, WINDOW_HEIGHT)

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

    def get_custom_zoom_view(self, world_surface, custom_zoom):
        """
        Retourne une vue de la caméra avec un zoom personnalisé.
        """
        # Calculer les dimensions de la vue en fonction du zoom personnalisé
        view_width = int(WINDOW_WIDTH / custom_zoom)
        view_height = int(WINDOW_HEIGHT / custom_zoom)

        # Calculer les coordonnées de la vue centrée sur la caméra
        center_x = self.camera_rect.x + self.camera_rect.width // 2
        center_y = self.camera_rect.y + self.camera_rect.height // 2
        view_rect = pygame.Rect(
            center_x - view_width // 2,
            center_y - view_height // 2,
            view_width,
            view_height
        )

        # Extraire la vue depuis la surface du monde
        custom_view = pygame.Surface((view_width, view_height))
        custom_view.blit(world_surface, (0, 0), view_rect)

        return custom_view
