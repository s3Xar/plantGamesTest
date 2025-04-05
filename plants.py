import pygame
import random

# Dimensiones de la ventana y la cuadrícula
WIDTH, HEIGHT = 1000, 800  # Aumentamos el tamaño de la ventana
GRID_SIZE = 10
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Tipos de celdas
EMPTY = 0
SOIL = 1
WATER = 2
PLANT_FAST = 3
PLANT_SLOW = 4
PLANT_PARASITIC = 5
SEED = 6

# Colores optimizados para la vista
BLACK = (30, 30, 30)
BROWN = (150, 111, 51)
BLUE = (100, 149, 237)
GREEN = (50, 205, 50)
DARK_GREEN = (34, 139, 34)
PURPLE = (186, 85, 211)
WHITE = (245, 245, 245)
YELLOW = (255, 215, 0)

# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Crear la cuadrícula inicial (agua y suelo aleatorio)
def generate_initial_grid():
    return [[SOIL if random.random() > 0.2 else WATER for _ in range(COLS)] for _ in range(ROWS)]

grid = generate_initial_grid()
plant_lifespans = {}  # Diccionario para almacenar la vida de cada planta

# Botones y estado
buttons = {
    "Start": pygame.Rect(10, 10, 80, 30),
    "Pause": pygame.Rect(100, 10, 80, 30),
    "Stop": pygame.Rect(190, 10, 80, 30),
    "Fast": pygame.Rect(300, 10, 80, 30),
    "Slow": pygame.Rect(390, 10, 80, 30),
    "Parasite": pygame.Rect(480, 10, 80, 30)
}
running = False
selected_plant = PLANT_FAST

# Dibujar la cuadrícula
def draw_grid():
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            color = (BROWN if grid[y][x] == SOIL else
                     BLUE if grid[y][x] == WATER else
                     GREEN if grid[y][x] == PLANT_FAST else
                     DARK_GREEN if grid[y][x] == PLANT_SLOW else
                     PURPLE if grid[y][x] == PLANT_PARASITIC else
                     YELLOW if grid[y][x] == SEED else
                     BLACK)
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Dibujar botones con texto
def draw_buttons():
    for text, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        screen.blit(font.render(text, True, BLACK), (rect.x + 10, rect.y + 5))

# Lógica de crecimiento y vida de plantas
def update_plants():
    global plant_lifespans
    new_grid = [row[:] for row in grid]
    new_lifespans = plant_lifespans.copy()
    
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] in (PLANT_FAST, PLANT_SLOW):
                if (x, y) in new_lifespans:
                    new_lifespans[(x, y)] -= 1
                    if new_lifespans[(x, y)] <= 0:
                        new_grid[y][x] = SEED if random.random() < 0.5 else SOIL  # 50% de probabilidad de semilla
                        new_lifespans.pop((x, y))
                    else:
                        spread_plant(new_grid, x, y, grid[y][x], chance=0.5 if grid[y][x] == PLANT_FAST else 0.2)
            elif grid[y][x] == SEED:
                if random.random() < 0.3:  # Probabilidad de germinar
                    new_grid[y][x] = PLANT_FAST if random.random() < 0.5 else PLANT_SLOW
                    new_lifespans[(x, y)] = 200 if new_grid[y][x] == PLANT_FAST else 100
            elif grid[y][x] == PLANT_PARASITIC:
                consumed = False
                for nx, ny in neighbors(x, y):
                    if grid[ny][nx] in [PLANT_FAST, PLANT_SLOW]:
                        new_grid[ny][nx] = PLANT_PARASITIC
                        new_lifespans[(nx, ny)] = -1
                        consumed = True
                        break
                if not consumed:
                    new_grid[y][x] = SOIL
    
    return new_grid, new_lifespans

def neighbors(x, y):
    return [(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if 0 <= nx < COLS and 0 <= ny < ROWS]

def spread_plant(grid, x, y, plant_type, chance):
    for nx, ny in neighbors(x, y):
        if grid[ny][nx] == SOIL and random.random() < chance:
            grid[ny][nx] = plant_type
            plant_lifespans[(nx, ny)] = 200 if plant_type == PLANT_FAST else 100

# Función principal
def main():
    global running, selected_plant, grid, plant_lifespans
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if name == "Start":
                            running = True
                        elif name == "Pause":
                            running = False
                        elif name == "Stop":
                            running = False
                            grid = generate_initial_grid()
                            plant_lifespans = {}
                        elif name == "Fast":
                            selected_plant = PLANT_FAST
                        elif name == "Slow":
                            selected_plant = PLANT_SLOW
                        elif name == "Parasite":
                            selected_plant = PLANT_PARASITIC
                        break
                else:
                    x, y = event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE
                    if 0 <= x < COLS and 0 <= y < ROWS and grid[y][x] == SOIL:
                        grid[y][x] = selected_plant
                        plant_lifespans[(x, y)] = 200 if selected_plant == PLANT_FAST else 100 if selected_plant == PLANT_SLOW else -1
        
        if running:
            grid, plant_lifespans = update_plants()
        
        draw_grid()
        draw_buttons()
        pygame.display.flip()
        clock.tick(10)
        # Limitar la velocidad de actualización

if __name__ == "__main__":
    main()