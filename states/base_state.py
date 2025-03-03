class BaseState():
    def __init__(self):
        pass

    def handle_event(self, event):
        """
        Gère les événements Pygame.
        """
        pass

    def update(self, dt, actions):
        """
        Mets à jour la logique de l'état (dt = delta time, actions = dict d'input).
        """
        pass

    def draw(self, screen):
        """
        Dessine l'état sur l'écran.
        """
        pass
