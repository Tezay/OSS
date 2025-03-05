import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from states.menu_state import MenuState
from input_manager import get_actions

# Classe pour gérer les différents état du jeu (les menus)
class StateManager:
    def __init__(self):
        self.current_state = None

    def set_state(self, new_state):
        self.current_state = new_state

# Fonction principale
def main():
    # Initialisation de pygame
    pygame.init()
    # Configuration des dimensions de la fenêtre (configurables depuis config.py)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Definition du titre de la fenêtre
    pygame.display.set_caption("OSS - Orbital Space Simulator")

    # Initialisation de la clock pygame
    clock = pygame.time.Clock()
    # Initialisation de la variable running (passe à False pour arrêter l'exécution du programme)
    running = True

    # Création du manager d'états
    state_manager = StateManager()
    # Création de MenuState (menu de démarrage)
    menu_state = MenuState(state_manager)
    # Attribution de MenuState au manager d'états (on passe l'état du manager à MenuState)
    state_manager.set_state(menu_state)

    # Boucle d'exécution (tourne tant que running est True)
    while running:
        # Première action, faire tourner la clock (en fonction du FPS spécifié dans config.py)
        dt = clock.tick(FPS) / 1000.0  # dt en secondes

        # Récupération des actions (touches) via input_manager
        actions = get_actions()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
            else:
                pos=(0,0)
            if event.type == pygame.QUIT:
                running = False
            # Délègue la gestion des événements (souris, etc.) à l'état courant
            if state_manager.current_state:
                state_manager.current_state.handle_event(event)


        # Mise à jour de l'état courant
        if state_manager.current_state:
            state_manager.current_state.update(dt, actions,pos)

        # Dessin de l'état courant
        if state_manager.current_state:
            state_manager.current_state.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
