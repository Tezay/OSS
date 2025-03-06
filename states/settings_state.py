import pygame


class SettingsState():
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

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

    def draw(self, screen,pos):
        screen.fill((0, 0, 0))

        pass
