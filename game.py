import pygame
import math
import os
from config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DEBUG_MODE,
    DEFAULT_SEED,
    NUMBER_OF_PLANETS,
    SPACESHIP_TEXTURE_DEFAULT_PATH,
    DEFAULT_PLANET_TEXTURE_PATH,
    RENDER_DISTANCE,
)
from map_generator import generate_map
from hud import Hud


class Game():
    """
    Classe qui gère la logique du "jeu en cours" :
    - Génération et stockage de la map
    - Caméra
    - Entités (planètes, vaisseau, etc.)
    - Méthodes update() et draw()
    """
    def __init__(self):
        
        self.planets = []
        self.planet_textures = {}
        self.spaceship = None
        self.hud = Hud()
        self.camera = None

        # Surface "monde" 
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.world.fill((20, 20, 64))

    def update(self, dt, actions):
        """
        Met à jour la logique du jeu (caméra, entités, etc.).
        dt = durée (en secondes) écoulée depuis la dernière frame
        actions = dictionnaire renvoyé par input_manager.get_actions()
        """
        # Mise à jour de la caméra (en mode debug, on bouge avec les touches)
        self.camera.update(actions)

        # Appliquer la gravité des planètes + collisions
        self.apply_gravity(dt)

        # Mettre à jour la physique du vaisseau (propulsion, etc.)
        if self.spaceship:
            self.spaceship.update_physics(dt)

        # Mise à jour de l'HUD
        self.hud.update(self.spaceship.vx, self.spaceship.vy)


    def set_planets(self, planets):
        """ Injecter la liste de planètes depuis l'extérieur. """
        self.planets = planets
        # Charger ou créer les textures
        self.planet_textures = {}
        # Pour chaque planète, on génère ou charge sa texture
        for planet in self.planets:
            texture_image = self.load_texture(planet)
            self.planet_textures[planet] = texture_image

    def load_texture(self, planet):
        """
        Chargement ou génération d'une texture pour la planète.
        La logique est la même qu'auparavant, adaptée sous forme de fonction.
        """

        # Vérifier s'il y a un chemin de texture spécifique
        if planet.texture != "":
            # Construire le chemin complet (par ex : "assets/planets/<nom>.png")
            texture_path = os.path.join(DEFAULT_PLANET_TEXTURE_PATH, f"{planet.texture}.png")
            try:
                # Tentative de chargement de l'image
                texture_image = pygame.image.load(texture_path).convert_alpha()
            except pygame.error:
                print(f"Failed to load texture for planet type '{planet.planet_type}'. Using default circle.")
                texture_image = None
        else:
            # Aucune texture spécifiée
            texture_image = None

        # Si aucune texture n'a pu être chargée, on dessine un cercle “par défaut”
        if texture_image is None:
            circle_size = planet.radius * 2
            texture_image = pygame.Surface((circle_size, circle_size), pygame.SRCALPHA)
            # Exemple : cercle magenta
            pygame.draw.circle(
                texture_image,
                (255, 0, 255),  # Couleur
                (planet.radius, planet.radius),  # Centre du cercle
                planet.radius  # Rayon
            )

        return texture_image

    def set_spaceship(self, spaceship):
        self.spaceship = spaceship

    def set_camera(self, camera):
        self.camera = camera

    def get_visible_planets(self):
        """
        Retourne la liste des planètes qui sont
        à moins de RENDER_DISTANCE du vaisseau.
        """
        visible = []
        if not self.camera:
            return visible

        sx, sy = self.camera.x, self.camera.y
        for planet in self.planets:
            dx = planet.x - sx
            dy = planet.y - sy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < RENDER_DISTANCE + planet.radius:
                visible.append(planet)

        return visible

    def apply_gravity(self, dt):
        """
        Calcule la force gravitationnelle exercée par les planètes proches
        sur le vaisseau, et gère la collision avec la surface si besoin.
        """
        pass

    def draw(self, screen):
        """
        Dessine le jeu sur l'écran (surface "screen").
        """
        # "Nettoyage" du fond (dans self.world)
        self.world.fill((0, 0, 50))
        
        # Dessiner les planètes visibles
        visible_planets = self.get_visible_planets()
        for planet in visible_planets:
            planet.draw(self.world)

        # Dessin du vaisseau
        self.spaceship.draw(self.world)

        # Affichage caméra
        view_surface, scaled_view = self._get_camera_view()
        screen.blit(scaled_view, (0, 0))

        # Dessin de l'HUD
        self.hud.draw(screen)

        # En mode debug, affichage d'infos
        if DEBUG_MODE:
            font = pygame.font.Font(None, 24)
            debug_text = f"Camera pos: ({self.camera.view_rect.x}, {self.camera.view_rect.y})  Zoom: {self.camera.zoom:.2f}  Seed: self.seed"
            text = font.render(debug_text, True, (255, 255, 255))
            screen.blit(text, (10, 10))

    # A revoir (+ commenter)
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
