import pygame
from .base_state import BaseState
from config import *
from gui.buttons import *



class MapFullScreen(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = custom_font
        self.world=game.world
        self.camera=self.game.camera
        self.surface=screen

    def handle_event(self, event, pos):
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["exit_current_menu"]:#or event.key==KEY_BINDINGS["open_map"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)
            
            if event.key==pygame.K_LEFT:
                #self.camera=self.game._get_camera_view()
                pass

    def update(self, dt, actions, pos, mouse_clicked):
        pass
    
    def draw(self, screen, pos):
        screen.fill((0, 0, 0))
        draw_buttons("test_add_item")

        #self.game.hud.draw_minimap(screen, self.game.camera, self.world)

        """
        Dessine la mini-map en utilisant une vue réduite de la caméra.
        """
        # Définir un zoom réduit pour la mini-map
        if DEBUG_MODE==True:
            minimap_zoom = 0.05  # Par exemple, 10% de la taille réelle
        else:
            minimap_zoom = 0.3  # Par exemple, 30% de la taille réelle



        # Obtenir une vue réduite de la caméra
        minimap_view = self.camera.get_custom_zoom_view(self.world, minimap_zoom)

        # Définir la position et la taille de la mini-map sur l'écran
        minimap_width = WINDOW_WIDTH
        minimap_height = WINDOW_HEIGHT
        minimap_x =0
        minimap_y =0

        # Redimensionner la vue réduite pour qu'elle corresponde à la taille de la mini-map
        # Note : usage de la fonction transform.smoothscale() au lieu de transform.scale()
        # pour appliquer un filtrage bilinéaire plus doux (étoiles de fond trop petites sinon)
        minimap_surface = pygame.transform.smoothscale(minimap_view, (minimap_width, minimap_height))

        # Dessiner la bordure grise autour de la mini-map
        border_rect = pygame.Rect(minimap_x - 2, minimap_y - 2, minimap_width + 4, minimap_height + 4)
        pygame.draw.rect(self.surface, (128, 128, 128), border_rect)

        # Dessiner la mini-map sur la surface principale
        self.surface.blit(minimap_surface, (minimap_x, minimap_y))

        # Dessiner le point représentant le vaisseau
        center_x = minimap_x + minimap_width // 2
        center_y = minimap_y + minimap_height // 2
        pygame.draw.circle(self.surface, (255, 0, 0), (center_x, center_y), 2)