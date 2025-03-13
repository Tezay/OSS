import pygame
import random
from config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DEBUG_MODE,
    DEFAULT_SEED,
    NUMBER_OF_PLANETS,
    SPACESHIP_TEXTURE_DEFAULT_PATH,
    DEFAULT_PLANET_TEXTURE_PATH,
)
from camera import Camera
from map_generator import generate_map
from spaceship import Spaceship
from hud import Hud
from states.settings_state.settings_menu_seed_state import custom_seed
import config


class Game():
    """
    Classe qui gère la logique du "jeu en cours" :
    - Génération et stockage de la map
    - Caméra
    - Entités (planètes, vaisseau, etc.)
    - Méthodes update() et draw()
    """
    def __init__(self):

        # Vérification si une custom_seed est toujours à None dans le module config
        if config.custom_seed is None:
            # Si c'est le cas, vérifie si DEFAULT_SEED est à None
            if DEFAULT_SEED is None:
                # Génère une seed aléatoire
                self.seed = random.randint(0, 999999999)
            else:
                # Sinon définie la seed à DEFAULT_SEED
                self.seed = DEFAULT_SEED
        else:
            # Sinon définie la seed à custom_seed
            self.seed=config.custom_seed
        print(f"Seed: {self.seed}")
        
        # Génération des planètes
        self.planets = generate_map(self.seed, WORLD_WIDTH, WORLD_HEIGHT, NUMBER_OF_PLANETS)
        print("Map generated.")

        # Création d'un dictionnaire vide des textures associées à chaque planète
        self.planet_textures = {}
        # Itération sur chaque planète
        for planet in self.planets:
            # Vérification si la planète a une texture associée
            if planet.texture != "":
                try:
                    # Définir le path de la texture
                    texture_path = f"{DEFAULT_PLANET_TEXTURE_PATH + planet.texture}.png"
                    # Convertir en image
                    texture_image = pygame.image.load(texture_path).convert_alpha()
                # Si erreur : mettre la texture à None
                except pygame.error:
                    print(f"Failed to load texture for {planet.planet_type}, using default circle.")
                    texture_image = None
            # Si aucune texture n'est associée à la planète, mettre à None
            else:
                texture_image = None

            # Si la texture n'est pas définie (None)
            if texture_image is None:
                # Création d'une surface transparente pour dessiner le cercle
                circle_size = planet.radius * 2  # Taille de l'image doit être au moins le diamètre de la planète
                texture_image = pygame.Surface((circle_size, circle_size), pygame.SRCALPHA)

                # Dessin du cercle au centre de la surface
                pygame.draw.circle(texture_image, (255, 0, 255), (planet.radius, planet.radius), planet.radius)

            # Ajout de la texture de la planète au dictionnaire de textures
            self.planet_textures[planet] = texture_image

        # Création de la surface "monde"
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.world.fill((20, 20, 64))

        # Test création du vaisseau
        self.spaceship = Spaceship(
            x=WORLD_WIDTH//2,
            y=WORLD_HEIGHT//2,
            vx=0, vy=0,
            width=20, height=20,
            image_path=SPACESHIP_TEXTURE_DEFAULT_PATH,
            mass=10
        )

        # Création de l'HUD
        self.hud = Hud()

        # Création de la caméra (à partir de la classe dédiée)
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        # Par défaut la caméra est centrée sur le vaisseau
        # Si le mode debug est désactivé, fournir une cible à la caméra
        if not DEBUG_MODE:
            # Le vaisseau est défini comme cible de la caméra
                self.camera.set_target(self.spaceship)

    def update(self, dt, actions):
        """
        Met à jour la logique du jeu (caméra, entités, etc.).
        dt = durée (en secondes) écoulée depuis la dernière frame
        actions = dictionnaire renvoyé par input_manager.get_actions()
        """
        # Mise à jour de la caméra (en mode debug, on bouge avec les touches)
        self.camera.update(actions)

        # Mise à jour de l'HUD
        self.hud.update(self.spaceship.vx, self.spaceship.vy)

    def draw(self, screen):
        """
        Dessine le jeu sur l'écran (surface "screen").
        """
        # "Nettoyage" du fond (dans self.world) si besoin
        self.world.fill((0, 0, 50))


        # Dessin des planètes
        for planet in self.planets:
            # Récupérer l'image chargée à l'initialisation
            original_texture = self.planet_textures[planet]

            # Mise à l'échelle : la planète fait 2*radius en largeur/hauteur
            diameter = planet.radius * 2
            scaled_texture = pygame.transform.scale(
                original_texture,
                (diameter, diameter)
            )

            # Pour centrer l'image sur (planet.x, planet.y)
            texture_rect = scaled_texture.get_rect()
            texture_rect.center = (planet.x, planet.y)

            # Dessiner l'image sur la surface du monde
            self.world.blit(scaled_texture, texture_rect)


        # Dessin du vaisseau
        self.spaceship.draw(self.world)

        # -- Affichage caméra -- #
        view_surface, scaled_view = self._get_camera_view()
        screen.blit(scaled_view, (0, 0))

        # Dessin de l'HUD
        self.hud.draw(screen)

        # En mode debug, affichage d'infos
        if DEBUG_MODE:
            font = pygame.font.Font(None, 24)
            debug_text = f"Camera pos: ({self.camera.view_rect.x}, {self.camera.view_rect.y})  Zoom: {self.camera.zoom:.2f}  Seed: {self.seed}"
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
