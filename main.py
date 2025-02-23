import pygame
import sys
import random
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DEBUG_MODE,
    DEFAULT_SEED,
    NUMBER_OF_PLANETS
)
from camera import Camera
from map_generator import generate_map

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("OSS - Orbital Space Simulator")

clock = pygame.time.Clock()

# On détermine la seed : si DEFAULT_SEED est None, on en génère une au hasard
if DEFAULT_SEED is None:
    seed = random.randint(0, 999999999)
else:
    seed = DEFAULT_SEED
print(f"Seed : {seed}")

# Génération de la liste de planètes
planets = generate_map(seed, WORLD_WIDTH, WORLD_HEIGHT, NUMBER_OF_PLANETS)
print("Planets generated.")

# Création d'une grande surface représentant le monde
world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
world.fill((20, 20, 64))  # Fond sombre pour simuler l'espace
print("World generated.")

# Exemple : vaisseau au centre du monde
ship_rect = pygame.Rect(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, 40, 40)
ship_color = (255, 255, 0)
pygame.draw.rect(world, ship_color, ship_rect)

# Création de la caméra
camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)

# En mode non-debug, la caméra suit le vaisseau
if not DEBUG_MODE:
    class Target:
        def __init__(self, rect):
            self.rect = rect
    camera.set_target(Target(ship_rect))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la caméra
    camera.update()

    # -- Rendu du monde avant affichage -- #
    # On "nettoie" le fond du monde à chaque frame (pour redessiner par-dessus)
    world.fill((0, 0, 50))

    # Dessin du vaisseau
    pygame.draw.rect(world, ship_color, ship_rect)

    # NEW : Dessin des planètes
    for planet in planets:
        pygame.draw.circle(world, planet.color, (planet.x, planet.y), planet.radius)

    # -- Création et affichage de la surface vue par la caméra -- #
    view_surface = pygame.Surface((camera.view_rect.width, camera.view_rect.height))
    border_color = (30, 30, 30)
    view_surface.fill(border_color)

    world_rect = pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
    intersection = camera.view_rect.clip(world_rect)

    if intersection.width > 0 and intersection.height > 0:
        dest_x = intersection.x - camera.view_rect.x
        dest_y = intersection.y - camera.view_rect.y
        dest_rect = pygame.Rect(dest_x, dest_y, intersection.width, intersection.height)
        view_surface.blit(world, dest_rect, intersection)

    scaled_view = pygame.transform.scale(view_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_view, (0, 0))

    # Affichage d'infos en mode debug
    if DEBUG_MODE:
        font = pygame.font.Font(None, 24)
        debug_text = f"Camera pos: ({camera.view_rect.x}, {camera.view_rect.y})  Zoom: {camera.zoom:.2f}  Seed: {seed}"
        text = font.render(debug_text, True, (255, 255, 255))
        screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
