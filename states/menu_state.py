import pygame
from .base_state import BaseState
from gui.buttons import *
from .game_state import GameState
from .settings_state.settings_menu_state import MenuSettingsState
from .credits_state import CreditsState
from config import WINDOW_WIDTH, WINDOW_HEIGHT, KEY_BINDINGS, DEBUG_MODE 

# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class MenuState(BaseState):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        # Exemple d'éléments à afficher
        self.title_font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 32)
        self.size = custom_size(16, 4)
        # Image de fond
        self.background_image = pygame.image.load("assets/menu_background.png").convert()

        # Liste images frame par frame de l'animation de la planète
        self.planet_frames = []

        # Charge image des frames
        spritesheet = pygame.image.load("assets/planet_spritesheet.png").convert_alpha()
        frame_width = 100
        frame_height = 100
        num_frames = 50

        # Redimensionne frame
        new_frame_height = WINDOW_HEIGHT // 2
        new_frame_width = new_frame_height

        # Itère sur chaque frame de l'animation
        for i in range(num_frames):
            # Def le rect correspondant à frame actuelle
            # Note : frame délimitée par : sa position (i * frame_width) et sa taille (frame_width, frame_height)
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            
            # Créer surface vide pour la frame
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            
            # Copier frame depuis spritesheet vers surface
            frame.blit(spritesheet, (0, 0), rect)

            # Redimensionne frame
            scaled_frame = pygame.transform.smoothscale(frame, (new_frame_width, new_frame_height))
            # Ajoute frame redimensionnée à liste
            self.planet_frames.append(scaled_frame)

        # Timer pour animation de planète
        self.current_planet_frame_index = 0
        self.planet_animation_timer = 0.0
        self.planet_frame_duration = 0.2

    def handle_event(self, event, pos):
        if event.type == pygame.KEYDOWN:
            # Vérification de la touche associée au démarrage du jeu
            if event.key == KEY_BINDINGS["start_game"]:
                from .game_state import GameState
                # Réinitialiser le timer persistant avant de lancer une nouvelle partie
                self.state_manager.reset_persistent_timer()
                # Passe l'état courant à game_state
                self.state_manager.set_state(GameState(self.state_manager))

    def update(self, dt, actions, pos, mouse_clicked):

        # Update animation planète
        self.planet_animation_timer += dt
        # Vérif si timer dépasse durée frame
        if self.planet_animation_timer >= self.planet_frame_duration:
            # Réduire timer de la durée d'une frame
            self.planet_animation_timer -= self.planet_frame_duration
            # Passer à l'index de la frame suivante
            self.current_planet_frame_index += 1
            # Si index dépasse nombre total de frames : revenir à première frame
            if self.current_planet_frame_index >= len(self.planet_frames):
                self.current_planet_frame_index = 0

        # Récupération des coordonnées de la souris
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("launch", pos, self.size):
                # Réinitialiser le timer persistant avant de lancer une nouvelle partie
                self.state_manager.reset_persistent_timer()
                # Passe l'état courant à game_state
                self.state_manager.set_state(GameState(self.state_manager))

            # Vérification du clique de la souris sur le bouton
            if click_button("menu_settings", pos, self.size):
                # Passe l'état courant à menu_settings_state
                self.state_manager.set_state(MenuSettingsState(self.state_manager))

            # Vérification du clique de la souris sur le bouton
            if click_button("quit", pos, self.size):
                # permet de quitter le programe dans le main via le bouton
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Vérification du clique de la souris sur le bouton Credits
            if click_button("credits", pos, self.size):
                self.state_manager.set_state(CreditsState(self.state_manager))

    def draw(self, screen, pos):

        # Dessin imag de fond
        screen.blit(self.background_image, (0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        # Dessin animation planète
        # Récup frame actuelle
        current_planet_frame = self.planet_frames[self.current_planet_frame_index]
        # Récup dimensions frame
        frame_width = current_planet_frame.get_width()
        frame_height = current_planet_frame.get_height()

        # Position frame sur l'écran
        gif_x = (WINDOW_WIDTH * 0.75) - (frame_width / 2)
        gif_y = (WINDOW_HEIGHT - frame_height) / 2
        # Dessin frame
        screen.blit(current_planet_frame, (gif_x, gif_y))

        if DEBUG_MODE:
            # Affiche la grille si on passe en paramètre True
            grille(True)

        # Dessin des boutons relatifs à l'état menu_state (avec la méthode .draw() de la classe Button)
        draw_size_buttons("launch", 6, 9, custom_size(16, 4))
        draw_size_buttons("menu_settings", 6, 14, custom_size(16, 4))
        draw_size_buttons("quit", 6, 24, custom_size(16, 4))
        draw_size_buttons("credits", 6, 19, custom_size(16, 4))

