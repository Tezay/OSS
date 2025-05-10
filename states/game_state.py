import pygame
import math
import random
import time
import os

from config import *
from .base_state import BaseState
from gui.buttons import *
from core.game import Game
from world.map_generator import generate_map
from entities.spaceship import Spaceship
from world.camera import Camera
import config
from core.json_manager import *
from systems.planet_resources import collect_planet_resources

# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class GameState(BaseState):
    def __init__(self, state_manager, existing_game=None):
        super().__init__()
        self.state_manager = state_manager
        self.font = custom_font
        self.pending_tutorial_state = False

        # Initialisation du timer de jeu via StateManager (si pas déjà fait)
        if self.state_manager.game_timer_start_time is None:
            self.state_manager.game_timer_start_time = time.time()

        # Vérification si un état game déjà crée a été transmis en paramètre
        # Note : Permet d'éviter de regénérer entièrement la map lors de changement d'état
        if existing_game is not None:
            # Réutilisation de l'existant (même map, même vaisseau, etc.)
            self.game = existing_game
            # Booléens pour enregistrer si les conseils ont déjà été affichés
            if not hasattr(self.game, 'first_tip_shown'):
                self.game.first_tip_shown = False
            if not hasattr(self.game, 'landing_tip_shown'):
                self.game.landing_tip_shown = False
            if not hasattr(self.game, 'resources_tip_shown'):
                self.game.resources_tip_shown = False
            
        # Sinon création d'un nouveau Game + nouvelle map + nouveau vaisseau
        else:
            # Création de la classe Game
            self.game = Game()
            # Initialisation des indicateurs de conseils (booléens)
            self.game.first_tip_shown = False
            self.game.landing_tip_shown = False
            self.game.resources_tip_shown = False

            # Selection de la seed
            if config.custom_seed is None:
                if DEFAULT_SEED is None:
                    seed = random.randint(0, 999999999)
                else:
                    seed = DEFAULT_SEED
            else:
                seed = config.custom_seed
            print(f"Seed: {seed}")

            # Génération de la map
            background_stars, self.planets = generate_map(seed, WORLD_WIDTH, WORLD_HEIGHT)
            print("Map generated.")

            # Injecter les étoiles et planètes dans Game
            self.game.set_background_stars(background_stars)
            self.game.set_planets(self.planets)

            # Création du vaisseau
            spaceship = Spaceship(
                x=WORLD_WIDTH//2,
                y=WORLD_HEIGHT//2,
                vx=0, vy=-10, # Vitesse par défaut de 10 pixel vers le haut
                width=23, height=23,
                image_path=SPACESHIP_TEXTURE_DEFAULT_PATH,
                mass=SPACESHIP_MASS
            )
            self.game.set_spaceship(spaceship)

            # Création de la caméra
            camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
            if not DEBUG_MODE:
                camera.set_target(spaceship)
            self.game.set_camera(camera)

            # Charge les dialogues d'introduction avec la fonction dédiée
            initial_dialogues = get_dialogues("initial_tutorial")
            # Si les dialogues existent, les charger dans l'HUD
            if initial_dialogues:
                self.game.hud.load_dialogues(initial_dialogues)
            else:
                print("Warning: Could not load initial tutorial dialogues.")
            
            # Si le joueur a pas terminé tuto, : l'afficher
            if not self.game.tutorial_completed_this_session and self.game.hud.show_dialogues:
                self.pending_tutorial_state = True

        # Booléen pour savoir si le son "engine_powered" et "ambiance" est en cours de lecture
        self.engine_sound_playing = False
        self.ambiance_sound_playing = False
        self.landed_sound_playing = False
        self.propulsion_sound_playing = False
        self.game.spaceship.propellant_alert_playing = False

        # Initialisation du timer afk
        self.afk_timer = 0
        self.last_time = pygame.time.get_ticks()  # Initialise une fois
        self.last_ship_pos = (0, 1000)  # Initialisation de la position initiale du vaisseau

        # Timer pour la mise à jour des ressources quand on est posé sur une planète
        self.landed_update_timer = 0.0

        self.tech_tree = self.game.data_manager.tech_tree.session_data

    def handle_event(self, event, pos):
        # Gestion des événements ponctuels

        if event.type == pygame.KEYDOWN:

            # Vérification de la touche associée au menu inventaire (si préssée, change l'état courant à inventory_state)
            if event.key == KEY_BINDINGS["inventory"]:
                from .inventory_state import InventoryState
                self.state_manager.set_state(InventoryState(self.state_manager, self.game))

            # Vérification de la touche associée au menu craft (si préssée, change l'état courant à crafting_state)
            if event.key == KEY_BINDINGS["crafting"]:
                from .crafting_state import CraftingState
                self.state_manager.set_state(CraftingState(self.state_manager, self.game))

            # Vérification de la touche associée au menu de paramètres (si préssée, change l'état courant à game_settings_state)
            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from .settings_state.settings_game_state import GameSettingsState
                self.state_manager.set_state(GameSettingsState(self.state_manager, self.game))

            # Ajout du passage à l'état Game Over avec "G"
            if event.key == KEY_BINDINGS["game_over"]:
                print("Game Over lancé !")
                from .game_over_state import GameOverState
                self.state_manager.set_state(GameOverState(self.state_manager, self.game))

            # Décélération instantanée (test, ne pas garder pour version finale)
            if event.key == KEY_BINDINGS["spaceship_deceleration"]:
                vx, vy = self.game.spaceship.vx, self.game.spaceship.vy
                speed = math.sqrt(vx**2 + vy**2)
                if speed > 1e-3:
                    decel_force = 3000
                    nx, ny = vx / speed, vy / speed
                    fx = -decel_force * nx
                    fy = -decel_force * ny
                    self.game.spaceship.add_force(fx, fy)

            # Arrêt instantané (mode debug)
            if DEBUG_MODE and event.key == KEY_BINDINGS["spaceship_stop"]:
                self.game.spaceship.vx = 0
                self.game.spaceship.vy = 0

        # Vérif si vaisseau est posé sur une planète ET si bouton souris cliqué
        if self.game.spaceship.is_landed and event.type == pygame.MOUSEBUTTONDOWN:
            # Récupération du rect du bouton "collecter" dans le HUD
            collect_rect = self.game.hud.collect_button_rect
            # Si le bouton "collecter" est cliqué
            if collect_rect and collect_rect.collidepoint(pos):
                # Appel de la fonction pour collecter les ressources de la planète
                collect_planet_resources(self.game.spaceship.landed_planet, self.game.data_manager.inventory)
                print("Collect resources button clicked!")
                # Joue le son de collecte de ressources
                self.game.sound_manager.play_sound("collect_resources", "collect_resources.wav")

    def update(self, dt, actions, pos, mouse_clicked):

        if hasattr(self, 'pending_tutorial_state') and self.pending_tutorial_state:
            self.pending_tutorial_state = False
            from .tutorial_state import TutorialState
            self.state_manager.set_state(TutorialState(self.state_manager, self.game))
            return

        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        if actions["open_map"]:
            from states.map_full_screen_state import MapFullScreen
            # Passe l'état courant à game_settings_state
            self.state_manager.set_state(MapFullScreen(self.state_manager, self.game))  # changer le state

        
        if mouse_clicked:
            # Vérification du clique de la souris sur le bouton
            if click_button('game_settings', pos, (20, 20)):
                from .settings_state.settings_game_state import GameSettingsState
                # Passe l'état courant à game_settings_state
                self.state_manager.set_state(GameSettingsState(self.state_manager, self.game))  # changer le state

                # Vérification du clique de la souris sur le bouton
            if click_button("tech_tree", pos, (20, 20)):
                from .tech_tree_state import TechTreeState
                # Définie l'état courant à TechTreeState
                # Note : self.game passé en paramètre, pour pouvoir récupérer la game en court (ne pas regénérer la map)
                self.state_manager.set_state(TechTreeState(self.state_manager, self.game))
                
            if click_button("inventory", pos, (20, 20)):
                from .inventory_state import InventoryState
                # Passe l'état courant à inventory_state
                self.state_manager.set_state(InventoryState(self.state_manager, self.game))
                
            if click_button("crafting", pos, (20, 20)):
                from .crafting_state import CraftingState
                # Passe l'état courant à crafting_state
                self.state_manager.set_state(CraftingState(self.state_manager, self.game))

        # Rotation gauche (si nitrogène > 0)
        if actions["spaceship_rotate_left"] and self.game.spaceship.nitrogen > 0:
            # Rotation du vaisseau (angle en degrés)
            self.game.spaceship.rotate(-SPACESHIP_ROTATION_SPEED * dt)
            # Mise à jour de l'image du vaisseau
            self.game.spaceship.update_image_angle()
            # Consommation de nitrogène
            self.game.spaceship.consume_nitrogen(0.2 * dt)
            # Activation de la texture RCS propulsion gauche
            self.game.spaceship.set_rcs_texture_state(True, "left")

        # Rotation droite (si nitrogène > 0)
        elif actions["spaceship_rotate_right"] and self.game.spaceship.nitrogen > 0:
            # Rotation du vaisseau (angle en degrés)
            self.game.spaceship.rotate(SPACESHIP_ROTATION_SPEED * dt)
            # Mise à jour de l'image du vaisseau
            self.game.spaceship.update_image_angle()
            # Consommation de nitrogène
            self.game.spaceship.consume_nitrogen(0.2 * dt)
            # Activation de la texture RCS propulsion droite
            self.game.spaceship.set_rcs_texture_state(True, "right")
      
        if actions["spaceship_rotate_left"] or actions["spaceship_rotate_right"]:
            # Si le vaisseau est en rotation, on joue le son de propulsion
            if not self.propulsion_sound_playing:
                self.game.sound_manager.play_sound("propulsion_sound", "propulsion_sound.wav")
                self.propulsion_sound_playing = True
       
        # Désactivation des textures RCS si aucune rotation    
        else:
            self.game.spaceship.set_rcs_texture_state(False)
        
            # Arrêter le son de propulsion si aucune rotation
            if self.propulsion_sound_playing:
                self.game.sound_manager.stop_sound("propulsion_sound")
                self.propulsion_sound_playing = False

        

        # Poussée continue si touche préssée (si propellant > 0)
        if actions["spaceship_move"] and self.game.spaceship.propellant > 0:

            # Active la texture powered quand la touche est préssée
            self.game.spaceship.set_powered_texture(True)

            # Conversion de l’angle en radians
            rad = math.radians(self.game.spaceship.angle)

            # Application de la force en direction du vaisseau
            print(self.tech_tree["tech_tree"]["ship_engine"]["tiers"]["tier_1"]["unlocked"])
            if self.tech_tree["tech_tree"]["ship_engine"]["tiers"]["tier_3"]["unlocked"]:
                print("4")
                SPACESHIP_THRUST_FORCE=SPACESHIP_THRUST_FORCE_T3
            elif self.tech_tree["tech_tree"]["ship_engine"]["tiers"]["tier_2"]["unlocked"]:
                print("3")
                SPACESHIP_THRUST_FORCE=SPACESHIP_THRUST_FORCE_T2
            elif self.tech_tree["tech_tree"]["ship_engine"]["tiers"]["tier_1"]["unlocked"]:
                print("2")
                SPACESHIP_THRUST_FORCE=SPACESHIP_THRUST_FORCE_T1
            elif self.tech_tree["tech_tree"]["ship_engine"]["tiers"]["tier_0"]["unlocked"]:
                print("1")
                SPACESHIP_THRUST_FORCE=SPACESHIP_THRUST_FORCE_T0
                
            fx = SPACESHIP_THRUST_FORCE * math.sin(rad)
            fy = -SPACESHIP_THRUST_FORCE * math.cos(rad)

            # Si le vaisseau est dans l'état atterri, lui permettre de redécoller
            if self.game.spaceship.is_landed:
                # Le booléen repasse à False 
                self.game.spaceship.is_landed = False
                # Application d'une force de poussé supplémentaire, pour facilité le décrochement du vaisseau de l'attraction gravitationnelle de la planète
                planet_mass = self.game.spaceship.landed_planet.mass
                # Arbitrairement, j'ai trouvé que la masse de la planète / 1e5*G fonctionnait bien
                takeoff_force_coeff = planet_mass/1e4
                self.game.spaceship.add_force(fx*takeoff_force_coeff, fy*takeoff_force_coeff)

            # Application de la force au vaisseau
            self.game.spaceship.add_force(fx, fy)

            # Jouer le son "engine_powered" si non déjà joué
            if not self.engine_sound_playing:
                self.game.sound_manager.play_sound("engine_powered", "engine_powered.ogg")
                self.engine_sound_playing = True
            
            # Consomme du propergol lors de la poussée
            self.game.spaceship.consume_propellant(0.5 * dt)

        else:
            # Désactiver la texture powered quand la touche est relâchée
            self.game.spaceship.set_powered_texture(False)

            # Arrêter le son "engine_powered" si la touche n'est plus préssée
            if self.engine_sound_playing:
                self.game.sound_manager.stop_sound("engine_powered")
                self.engine_sound_playing = False

        # Update du game (renvoie un booléen si le vaisseau est détruit)
        dead = self.game.update(dt, actions)

        # Si l'update du jeu renvoie que le joueur est mort
        if dead:
            # vérification si le vaisseau a été détruit (respawning = True)
            global respawning
            # Gestion du respawn reset du vaisseau
            if config.respawning:
                print("Respawn detected ! Spaceship reset...")
                # Réinitialise la position du vaisseau
                self.game.spaceship.reset()
                # Réinitialise la variable globale respawning à False
                config.respawning = False

            # Passe l'état courant à GameOverState
            from states.game_over_state import GameOverState
            self.state_manager.set_state(GameOverState(self.state_manager, self.game))
            print("Game Over triggered")
        
        # anti-Afk
        # Initialisation du timer avec Pygame
        current_ship_pos = (self.game.spaceship.x, self.game.spaceship.y)
        current_time_afk = pygame.time.get_ticks()
        # Vérification si une touche est préssée
        if ( not (math.isclose(current_ship_pos[0], self.last_ship_pos[0], abs_tol=0.001) and math.isclose(current_ship_pos[1], self.last_ship_pos[1], abs_tol=0.001 ))):
            self.game.afk_timer = 0
            self.last_ship_pos = current_ship_pos
            self.last_time = current_time_afk  # Met à jour le temps actuel
        else:
            # Vérifie si une seconde (1000 ms) est passée
            if current_time_afk - self.last_time >= 1000:
                self.game.afk_timer += 1
                self.last_time = current_time_afk  # Met à jour le temps actuel

        # Si le joueur est afk depuis 90 secondes déclenche l'état AFK (NE MARCHE PAS )
        if (self.game.afk_timer > AFK_TIME):
            from .afk_state import AFKState
            self.state_manager.set_state(AFKState(self.state_manager, self.game))
            print("AFK triggered")

        # Mise à jour des ressources si le vaisseau est posé
        if self.game.spaceship.is_landed:
            self.landed_update_timer += dt
            # Toutes les 10 secondes
            if self.landed_update_timer >= 10.0:
                landed_planet = self.game.spaceship.landed_planet
                if landed_planet:
                    landed_planet.update_resources_while_landed()
                # Réinitialise le timer pour la prochaine mise à jour
                self.landed_update_timer -= 10.0

        # Mise à jour du timer de jeu via StateManager
        current_time = time.time()
        elapsed_since_start = current_time - self.state_manager.game_timer_start_time
        self.state_manager.persistent_game_timer_value = max(0, GAME_TIMER_DURATION - elapsed_since_start)
        
        # Vérif pour afficher conseil récup fuel
        if ( not self.game.first_tip_shown and self.game.spaceship.propellant < SPACESHIP_MAX_PROPELLANT - 20 ) or self.game.spaceship.propellant < 15:
            self.game.first_tip_shown = True
            self.game.hud.add_info_box("first_tip")
            print("Affichage de la première mission")
        
        # Vérif pour afficher conseil atterrissage
        if not self.game.landing_tip_shown and self.game.hud.resultant_force > 8:
            self.game.landing_tip_shown = True
            self.game.hud.add_info_box("landing_tip")
            print("Affichage de la mission d'atterrissage")

        # Vérif pour afficher conseil ressources
        if not self.game.resources_tip_shown:
            self.game.resources_tip_shown = True
            self.game.hud.add_info_box("resources_tip")
            print("Affichage de la mission ressources")

        # Vérifie en permanence si le vaisseau n'est pas détruit ou posé avant de jouer le son d'ambiance
        if not dead and not self.game.spaceship.is_landed:
            if not self.ambiance_sound_playing: 
                random_sound = random.choice(["ambiance_1.wav", "ambiance_2.wav", "ambiance_3.wav", "ambiance_4.wav", "ambiance_5.wav", "ambiance_6.wav"])
                print(f"Loading sound: {random_sound}")
                name_without_extension, extension = os.path.splitext(random_sound)
                self.game.sound_manager.play_sound(name_without_extension, random_sound)
                self.ambiance_sound_playing = True
                self.ambiance_wait_timer = pygame.time.get_ticks()  # Start the timer
                random_sound_path = os.path.join("assets/sounds", random_sound)
                self.current_ambiance_duration = pygame.mixer.Sound(random_sound_path).get_length() * 1000  # Récupérer la durée du son en millisecondes

            if self.ambiance_sound_playing:
                play_or_not = random.choice([ultra_pause, long_pause, short_pause, mini_pause])
                current_time_song = pygame.time.get_ticks()
                # Vérifie si le son d'ambiance a été joué pendant la durée spécifiée
                if current_time_song - self.ambiance_wait_timer >= self.current_ambiance_duration + play_or_not * 1000:
                    self.ambiance_sound_playing = False
        else:
            # Arrête le son d'ambiance si le vaisseau est détruit ou posé
            if self.ambiance_sound_playing:
                self.game.sound_manager.stop_sound("ambiance")
                self.ambiance_sound_playing = False


        # Son pour l'atterrissage du vaisseau sur une planète
        if self.game.spaceship.is_landed:
            # Si le vaisseau est posé sur une planète et que le son n'est pas déjà joué
            if not self.landed_sound_playing:
                # Joue le son d'atterrissage
                random_sound_landed = random.choice(["success_landing.ogg", "success_landing_2.ogg"])
                print(f"Loading sound: {random_sound_landed}")
                name_without_extension_landed, extension = os.path.splitext(random_sound_landed)
                self.game.sound_manager.play_sound(name_without_extension_landed, random_sound_landed)
                # Marque le son comme joué
                self.landed_sound_playing = True
        if not self.game.spaceship.is_landed:
            self.landed_sound_playing = False
            

        # Son d'alerte pour le vaisseau (si propellant < 10% de la capacité max)
        if (self.game.spaceship.propellant < SPACESHIP_MAX_PROPELLANT * 0.1 ):
            if not self.game.spaceship.propellant_alert_playing:
                # Joue le son d'alerte
                self.game.sound_manager.play_sound("propellant_alert", "propellant_alert.wav")
                # Marque le son comme joué
                self.game.spaceship.propellant_alert_playing = True

        if (self.game.spaceship.propellant >= SPACESHIP_MAX_PROPELLANT * 0.1) :
            self.game.spaceship.propellant_alert_playing = False

        # Son d'alerte pour le vaisseau (si nitrogen < 10% de la capacité max)
        if (self.game.spaceship.nitrogen < SPACESHIP_MAX_NITROGEN * 0.1 ):
            if not self.game.spaceship.nitrogen_alert_playing:
                # Joue le son d'alerte
                self.game.sound_manager.play_sound("propellant_alert", "propellant_alert.wav")
                # Marque le son comme joué
                self.game.spaceship.nitrogen_alert_playing = True

        if (self.game.spaceship.nitrogen >= SPACESHIP_MAX_NITROGEN * 0.1) :
            self.game.spaceship.nitrogen_alert_playing = False



    def draw(self, screen, pos):

        # Récup la valeur actuelle du timer persistant depuis le StateManager pour afficher
        timer_value_to_display = self.state_manager.persistent_game_timer_value
        
        # Dessin du jeu (espace 2d avec planètes et vaisseau, HUD, minimap etc.)
        self.game.draw(screen, persistent_game_timer_value=timer_value_to_display)

        nitrogen=self.game.spaceship.nitrogen
        propellant=self.game.spaceship.propellant

        #print(propellant,nitrogen)

        if propellant==SPACESHIP_MAX_PROPELLANT:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant\propellant_max.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*90:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_9.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*80:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_8.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*70:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_7.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*60:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_6.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*50:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_5.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*40:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_4.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*30:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_3.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*20:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_2.png").convert_alpha()
        elif propellant>(SPACESHIP_MAX_PROPELLANT/100)*10:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_1.png").convert_alpha()
        else:
            propellant_image=pygame.image.load(HUD_TEXTURE_PATH+"propellant/propellant_0.png").convert_alpha()

        coord_hud=hud_draw(38,31,50,35)
        screen.blit(propellant_image, coord_hud)

        
        if nitrogen==SPACESHIP_MAX_NITROGEN:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_max.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*90:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_9.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*80:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_8.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*70:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_7.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*60:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_6.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*50:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_5.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*40:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_4.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*30:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_3.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*20:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_2.png").convert_alpha()
        elif nitrogen>(SPACESHIP_MAX_NITROGEN/100)*10:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_1.png").convert_alpha()
        else:
            nitrogen_image=pygame.image.load(HUD_TEXTURE_PATH+"nitrogen/nitrogen_0.png").convert_alpha()

        coord_hud=hud_draw(38,33,50,35)
        screen.blit(nitrogen_image, coord_hud)

        # Affichage du message d'alerte pour l'afk
        if (self.game.afk_timer > AFK_TIME-10):
            self.font = custom_font
            warning_text = self.font.render(f"Il vous reste {AFK_TIME - self.game.afk_timer} secondes avant d'être AFK", True, (255, 0, 0))
            ect = warning_text.get_rect(center=screen.get_rect().center)
            screen.blit(warning_text, ect)

        if self.game.spaceship.is_landed:
            planet = self.game.spaceship.landed_planet
            current_time_seconds = pygame.time.get_ticks() / 1000.0

            # Si la planète n'a pas encore été marquée comme visitée dans cette session d'atterrissage
            if not planet.visited:
                # Vérifier si elle a déjà été visitée auparavant (last_visited_time existe)
                if planet.last_visited_time is not None:
                    elapsed_time = current_time_seconds - planet.last_visited_time
                    # Mettre à jour les ressources générées pendant l'absence
                    planet.update_resources_offline(elapsed_time)

                # Marquer la planète comme visitée et enregistrer le temps actuel
                planet.visited = True
                planet.last_visited_time = current_time_seconds

            mouse_x, mouse_y = pygame.mouse.get_pos()
            color = screen.get_at((mouse_x, mouse_y))

            radius=self.game.spaceship.landed_planet.radius
            info = pygame.display.Info()
            spaceship_x=info.current_w//2
            spaceship_y=info.current_h//2

            distance = math.sqrt((mouse_x - spaceship_x) ** 2 + (mouse_y - spaceship_y) ** 2)
            if color != (0,0,50,255) and distance<=radius*3:
                planet_info = planet.planet_type

                # Construction du texte pour l'overlay avec les quantités actuelles
                resource_texts = []
                # Trie des ressources par nom
                sorted_resource_names = sorted(planet.resources.keys())
                for resource_name in sorted_resource_names:
                    quantity = planet.resources[resource_name]
                    # Affichage des ressources et quantités
                    resource_texts.append(f"- {resource_name}: {quantity:.0f}")

                if not resource_texts:
                    ressource_display = "Aucune ressource disponible"
                else:
                    ressource_display = "\n ".join(resource_texts)

                txt = f"{planet.name} ({planet_info})\n Ressources actuelles :\n {ressource_display}"
                overlay(txt, pygame.mouse.get_pos())

        from gui.ressources_mined import RessourcesMined
        planets=RessourcesMined(self.game).update()


