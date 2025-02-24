import pygame
from config import KEY_BINDINGS

def get_actions():
    """
    Retourne un dictionnaire contenant l'état des actions définies dans KEY_BINDINGS.
    Par ex: {"camera_left": True, "camera_right": False, "pause": False, ...}
    """
    keys = pygame.key.get_pressed()
    actions = {}

    # On parcourt toutes les actions définies dans config.py
    for action_name, key_code in KEY_BINDINGS.items():
        actions[action_name] = keys[key_code]
    
    return actions
