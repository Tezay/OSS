import pygame
import math
import os

from config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DEBUG_MODE,
    DEFAULT_PLANET_TEXTURE_PATH,
    RENDER_DISTANCE,
    G,
    MAX_LANDING_SPEED,
    LANDING_DAMPING_FACTOR
)
from gui.hud import Hud
from core.session_data_manager import DataManager
from core.sound_manager import SoundManager


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
        self.background_stars = []
        self.planet_textures = {}
        self.spaceship = None
        self.hud = Hud()
        self.camera = None
        self.data_manager = DataManager()
        self.sound_manager = SoundManager()

        # Surface "monde" 
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.world.fill((20, 20, 64))

        self.afk_timer = 0  # Timer anti-AFK

    def update(self, dt, actions):
        """
        Met à jour la logique du jeu (caméra, entités, etc.).
        dt = durée (en secondes) écoulée depuis la dernière frame
        actions = dictionnaire renvoyé par input_manager.get_actions()
        """
        # Mise à jour de la caméra (en mode debug, on bouge avec les touches)
        self.camera.update(actions)
        #print("ppppppppppppppppppp",self.camera)

        # Appliquer la gravité des planètes + collisions 
        # Renvoie un booléen pour savoir si le vaisseau est rentré en collision avec la planète
        deadly_collision = self.apply_gravity(dt)

        # Mettre à jour la physique du vaisseau (propulsion, etc.)
        if self.spaceship:
            self.spaceship.update_physics(dt)

        # Mise à jour de l'HUD
        self.hud.update(self.spaceship.x, self.spaceship.y, self.spaceship.vx, self.spaceship.vy, self.spaceship.propellant, self.spaceship.nitrogen)
      
        return deadly_collision

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

    def set_background_stars(self, stars):
        """ Injecter la liste d'étoiles de fond depuis l'extérieur. """
        self.background_stars = stars

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

    def compute_net_forces(self, x, y, mass):
        """
        Calcule la somme des forces (gravité, etc.) sur un objet
        de masse 'mass' situé à (x, y).
        Retourne (fx_total, fy_total).
        """
        fx_total = 0.0
        fy_total = 0.0

        # Parcours des planètes visibles
        visible_planets = self.get_visible_planets()
        for planet in visible_planets:
            # Calcul de la gravité
            dx = planet.x - x
            dy = planet.y - y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 1e-6:
                continue
            
            # F = G*(m1*m2)/(d^2)
            force = G * (planet.mass * mass) / (dist*dist)
            
            # Projection sur x,y
            fx_total += force * (dx/dist)
            fy_total += force * (dy/dist)

        return fx_total, fy_total
    
    def check_collision_and_land(self, x, y, vx, vy, radius_vaisseau, dt):
        """
        Vérifie s'il y a collision entre le vaisseau (position x, y, rayon radius_vaisseau)
        et une planète. 
        - x, y, vx, vy sont les coordonnées et vitesse de l'objet
        - dt est la durée du pas de temps qu'on vient de simuler
        - Retourne (new_x, new_y, new_vx, new_vy, landed) 
        où 'landed' indique si on a atterri sur une planète.

        On considère l'atterrissage réussi si la vitesse < MAX_LANDING_SPEED.
        On recalcule la position (x,y) en cas de chevauchement pour coller à la surface.
        """
        landed = False
        landed_planet = None
        # Récupère les planètes visibles
        visible_planets = self.get_visible_planets()
        
        # Itère sur les planètes visibles
        for planet in visible_planets:

            # Calcul de la distance entre le vaisseau et la planète
            dist_centers = math.sqrt((planet.x - x)**2 + (planet.y - y)**2)
            # Calcul de la distance de collision
            collision_dist = planet.radius + radius_vaisseau

            # Initialisation de la variable deadly_collision
            deadly_collision = False

            # Si distance entre vaisseau et planète <= rayon planète + vaisseau
            # Alors il y a collision, et il faut regarder si le vaisseau atterri
            if dist_centers <= collision_dist:

                # Calcul de la vitesse du vaisseau
                speed = math.sqrt(vx*vx + vy*vy)

                # Seulement si on n’est PAS déjà posé :
                if not self.spaceship.is_landed:

                    # Si le vaisseau est 2 fois plus rapide que la vitesse d'atterrissage max
                    if speed >= MAX_LANDING_SPEED *2:
                        # Collision mortel avec une planète passe deadly_collision à True pour faire respawn le vaisseau
                        deadly_collision = True
                        print("Deadly collision with a planet!")
                        # Sortir de la boucle d'itération des planètes dès lors qu'on sait qu'il y a une collision mortelle avec l'une d'elles
                        break
 
                    # Si le vaisseau est plus rapide que la vitesse d'atterrissage max, mais moins que 2 fois
                    elif speed >= MAX_LANDING_SPEED:
                        # Collision brutale : fait un rebond
                        overlap = collision_dist - dist_centers
                        # Exerce une vitesse dans l'autre sans
                        nx = (x - planet.x) / (dist_centers + 1e-6)
                        ny = (y - planet.y) / (dist_centers + 1e-6)
                        x += nx * overlap
                        y += ny * overlap
                        vx = -vx * LANDING_DAMPING_FACTOR
                        vy = -vy * LANDING_DAMPING_FACTOR
                    
                    # Sinon le vaisseau a une vitesse d'atterrissage
                    else:
                        # Atterrisage
                        landed = True
                        landed_planet = planet

                else:
                    # Le vaisseau est déjà "landed"
                    # Recaler le vaisseau pour s'assurer qu'il ne s'enfonce pas
                    overlap = collision_dist - dist_centers
                    nx = (x - planet.x) / (dist_centers + 1e-4)
                    ny = (y - planet.y) / (dist_centers + 1e-4)
                    x += nx * overlap
                    y += ny * overlap
        
        # Jouer le son "explosion" si deadly_collision est True
        if deadly_collision:
            # Arrête le son "engine_powered" et joue le son "explosion"
            self.sound_manager.stop_sound("engine_powered")
            self.sound_manager.play_sound("explosion", "explosion.ogg")
        
            # Change la texture du vaisseau en exploded
            self.spaceship.set_exploded_texture(True)

        return (x, y, vx, vy, landed, landed_planet, deadly_collision)

    def predict_spaceship_trajectory(self, steps=200, dt_sim=0.08):
        if not self.spaceship:
            return []

        sim_x = self.spaceship.x
        sim_y = self.spaceship.y
        sim_vx = self.spaceship.vx
        sim_vy = self.spaceship.vy
        sim_mass = self.spaceship.mass

        points = [(sim_x, sim_y)]

        for _ in range(steps):
            fx, fy = self.compute_net_forces(sim_x, sim_y, sim_mass)
            ax = fx / sim_mass
            ay = fy / sim_mass
            sim_vx += ax * dt_sim
            sim_vy += ay * dt_sim
            sim_x += sim_vx * dt_sim
            sim_y += sim_vy * dt_sim
            points.append((sim_x, sim_y))

        return points

    def apply_gravity(self, dt):
        """
        Calcule la force gravitationnelle exercée par les planètes proches
        sur le vaisseau, et gère la collision avec la surface si besoin.
        """
        if not self.spaceship:
            return

        # Calculer la force résultante
        fx, fy = self.compute_net_forces(self.spaceship.x, self.spaceship.y, self.spaceship.mass)

        # Appliquer cette force
        self.spaceship.add_force(fx, fy)

        # Répéter la même chose une seconde fois
        # Note : Je sais pas pourquoi, mais la trajectoire du vaisseau fonctionne mieux en faisant ça
        fx, fy = self.compute_net_forces(self.spaceship.x, self.spaceship.y, self.spaceship.mass)
        self.spaceship.add_force(fx, fy)

        # Passer les forces à l'HUD pour l'affichage de l'indicateur de force
        self.hud.fx_indicator, self.hud.fy_indicator = fx, fy
        
        # Mettre à jour la physique du vaisseau
        self.spaceship.update_physics(dt)

        # Gérer la collision (pour atterrissage)
        radius_vaisseau = min(self.spaceship.rect.width, self.spaceship.rect.height)/2
        new_x, new_y, new_vx, new_vy, just_landed, landed_planet, deadly_collision = self.check_collision_and_land(
            self.spaceship.x,
            self.spaceship.y,
            self.spaceship.vx,
            self.spaceship.vy,
            radius_vaisseau,
            dt
        )

        # Appliquer les changements
        self.spaceship.x = new_x
        self.spaceship.y = new_y
        self.spaceship.vx = new_vx
        self.spaceship.vy = new_vy

        # Passe l'état du vaisseau comme atterri
        if just_landed:
            self.spaceship.is_landed = True
            # Transmet la planète sur laquelle le vaisseau a atterri
            self.spaceship.landed_planet = landed_planet
            print(f"Successful landing on {landed_planet.name}!")
        
        return deadly_collision


    def draw(self, screen, respawning=False):
        """
        Dessine le jeu sur l'écran (surface "screen").
        """
        # "Nettoyage" du fond (dans self.world)
        self.world.fill((0, 0, 50))

        self.world_wiouth_stars = self.world
        # Dessiner les étoiles de fond directement sur le fond
        for star in self.background_stars:
            half_size = star.size // 2
            pygame.draw.rect(
                self.world,
                star.color,
                (star.x - half_size, star.y - half_size, star.size, star.size)
            )

        # Dessiner les planètes visibles
        visible_planets = self.get_visible_planets()
        for planet in visible_planets:
            planet.draw(self.world)

        # Dessin du vaisseau
        self.spaceship.draw(self.world)

        # Affichage caméra
        view_surface, scaled_view = self._get_camera_view()
        screen.blit(scaled_view, (0, 0))

        # Dessiner la trajectoire du vaisseau
        if self.spaceship and not respawning:
            trajectory_points = self.predict_spaceship_trajectory()

            # Récupérer les dimensions actuelles de la fenêtre
            current_window_width = pygame.display.get_surface().get_width()
            current_window_height = pygame.display.get_surface().get_height()

            # Transformer tous les points en coordonnées écran
            transformed_points = []
            for (px, py) in trajectory_points:
                dx = px - self.camera.view_rect.x
                dy = py - self.camera.view_rect.y
                dx *= (current_window_width / self.camera.view_rect.width)
                dy *= (current_window_height / self.camera.view_rect.height)
                transformed_points.append((dx, dy))

            if len(transformed_points) > 1:
                # Paramètres des pointillés
                segment_length = 5  # Longueur d'un segment
                gap_length = 5      # Longueur d'un espace

                # Dessiner les segments
                current_length = 0
                draw_segment = True  # Commence par dessiner
                
                for i in range(len(transformed_points)-1):
                    start = transformed_points[i]
                    end = transformed_points[i+1]
                    
                    # Calcul de la longueur du segment actuel
                    dx = end[0] - start[0]
                    dy = end[1] - start[1]
                    segment_dist = math.sqrt(dx*dx + dy*dy)
                    
                    # Vérification pour éviter division par zéro
                    if segment_dist > 0:
                        if draw_segment:
                            pygame.draw.line(screen, (255, 255, 255), start, end, 2)
                        
                        # Mise à jour de la longueur cumulée
                        current_length += segment_dist
                        if current_length >= (segment_length if draw_segment else gap_length):
                            current_length = 0
                            draw_segment = not draw_segment

        # Dessin de l'HUD avec la caméra et la surface du monde
        self.hud.draw(screen, self.camera, self.world,self.world_wiouth_stars)

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
    

