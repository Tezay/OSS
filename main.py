import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from states.menu_state import *
from core.input_manager import get_actions


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

    mouse_clicked = False
    mouse_pos = (0, 0)
    previous_state = None

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

        # Vérifier si l'état a changé
        if state_manager.current_state != previous_state:
            mouse_clicked = False  # Annuler tout clic en cours lors d'un changement d'état
            previous_state = state_manager.current_state
        else:
            mouse_clicked = False  # Réinitialiser l'état du clic à chaque frame

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                mouse_clicked = True
            if event.type == pygame.QUIT:
                running = False
            if state_manager.current_state:
                state_manager.current_state.handle_event(event, mouse_pos)

        # Mise à jour de l'état courant
        if state_manager.current_state:
            state_manager.current_state.update(dt, actions, mouse_pos, mouse_clicked)

        # Dessin de l'état courant
        if state_manager.current_state:
            state_manager.current_state.draw(screen, mouse_pos)

        # Affichage du FPS
        fps_surface = custom_font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_surface, (20, -4))

        # Refresh de l'affichage pygame
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
