from .base_state import BaseState
from buttons import *
from config import custom_font


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class InventoryState(BaseState):
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = pygame.font.Font(None, 50)

    def handle_event(self, event,pos):
        # Gestion des événements ponctuels
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_BINDINGS["inventory"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

    def update(self, dt, actions, pos, mouse_clicked):

        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos

        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("return",pos):
                from states.game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)
            
            ########### TEST ############
            # Exemple de bouton pour tester l'ajout/suppression d'un item dans l'inventaire
            if click_button('test_add_item',pos):
                self.game.data_manager.inventory.add_item("test_item", 2)
            if click_button('test_remove_item',pos):
                self.game.data_manager.inventory.remove_item("test_item", 2)
            #############################

    def draw(self, screen,pos):

        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Dessin du texte
        self.font = custom_font
        text_surf = self.font.render("Inventaire - appuyez sur I pour reprendre", True, (255, 255, 255))
        rect = text_surf.get_rect(center=screen.get_rect().center)

        
        ########### TEST ############
        # Exemple de bouton pour tester l'upgrade d'un module du tech tree
        draw_buttons("test_add_item")
        draw_buttons("test_remove_item")
        #############################

        screen.blit(text_surf, rect)
