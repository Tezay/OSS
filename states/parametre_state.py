import pygame


class parametreState():
    def __init__(self, state_manager, game):
        super().__init__()
        self.state_manager = state_manager
        self.game = game
        self.font = pygame.font.Font(None, 50)

    def handle_event(self, event):
        """
        Gère les événements Pygame.
        """
        pass

    def update(self, dt, actions,pos):
        """
        Mets à jour la logique de l'état (dt = delta time, actions = dict d'input).
        """
        pass

    def draw(self, screen):
        """
        Dessine l'état sur l'écran.
        """
        pass
