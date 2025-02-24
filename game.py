import pygame
import random
from config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DEBUG_MODE,
    DEFAULT_SEED,
    NUMBER_OF_PLANETS,
    FPS
)
from camera import Camera
from map_generator import generate_map

class Game:
    """
    Classe qui gère la logique du "jeu en cours" :
    - Génération et stockage de la map
    - Caméra
    - Entités (planètes, vaisseau, etc.)
    - Méthodes update() et draw()
    """
    def __init__(self):
        # Génération de la seed si aucune est spécifiée par défaut
        if DEFAULT_SEED is None:
            self.seed = random.randint(0, 999999999)
        else:
            self.seed = DEFAULT_SEED
        
        print(f"Seed: {self.seed}")
        # Génération des planètes
        self.planets = generate_map(self.seed, WORLD_WIDTH, WORLD_HEIGHT, NUMBER_OF_PLANETS)
        print("Map generated.")

        # Création de la surface "monde"
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.world.fill((20, 20, 64))

        # Création d'un vaisseau pour l'exemple
        # C'est juste pour illustrer, faudra faire un truc plus tard
        self.ship_rect = pygame.Rect(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, 40, 40)
        self.ship_color = (255, 255, 0)
        pygame.draw.rect(self.world, self.ship_color, self.ship_rect)

        # Création de la caméra (à partir de la classe dédiée)
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        # Par défaut la caméra est centrée sur le vaisseau
        # Si le mode debug est désactivé, on fourni une cible à la caméra
        if not DEBUG_MODE:
            # Suivi du vaisseau
            class Target:
                def __init__(self, rect):
                    self.rect = rect
            self.camera.set_target(Target(self.ship_rect))

    def update(self, dt, actions):
        """
        Met à jour la logique du jeu (caméra, entités, etc.).
        dt = durée (en secondes) écoulée depuis la dernière frame
        actions = dictionnaire renvoyé par input_manager.get_actions()
        """
        # Mise à jour de la caméra (en mode debug, on bouge avec les touches)
        self.camera.update(actions)

    def draw(self, screen):
        """
        Dessine le jeu sur l'écran (surface "screen").
        """
        # "Nettoyage" du fond (dans self.world) si besoin
        self.world.fill((0, 0, 50))

        # Dessin du vaisseau
        pygame.draw.rect(self.world, self.ship_color, self.ship_rect)

        # Dessin des planètes
        for planet in self.planets:
            pygame.draw.circle(self.world, planet.color, (planet.x, planet.y), planet.radius)

        # -- Affichage caméra -- #
        view_surface, scaled_view = self._get_camera_view()
        screen.blit(scaled_view, (0, 0))

        # En mode debug, affichage d'infos
        if DEBUG_MODE:
            font = pygame.font.Font(None, 24)
            debug_text = f"Camera pos: ({self.camera.view_rect.x}, {self.camera.view_rect.y})  Zoom: {self.camera.zoom:.2f}  Seed: {self.seed}"
            text = font.render(debug_text, True, (255, 255, 255))
            screen.blit(text, (10, 10))

    def _get_camera_view(self):
        """ 
        Gère la logique d'extraction de la vue depuis self.world en fonction de la caméra.
        Retourne (view_surface, scaled_view).
        """
        view_surface = pygame.Surface((self.camera.view_rect.width, self.camera.view_rect.height))
        border_color = (30, 30, 30)
        view_surface.fill(border_color)

        world_rect = pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        intersection = self.camera.view_rect.clip(world_rect)

        if intersection.width > 0 and intersection.height > 0:
            dest_x = intersection.x - self.camera.view_rect.x
            dest_y = intersection.y - self.camera.view_rect.y
            dest_rect = pygame.Rect(dest_x, dest_y, intersection.width, intersection.height)
            view_surface.blit(self.world, dest_rect, intersection)

        scaled_view = pygame.transform.scale(view_surface, (pygame.display.get_surface().get_width(), 
                                                            pygame.display.get_surface().get_height()))
        return view_surface, scaled_view
