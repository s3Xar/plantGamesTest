import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 5
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
SAND = 1
WATER = 2
SOIL_DRY = 3
SOIL_WET = 4
SEED = 5
GRASS = 6

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# UI Buttons
sand_button = pygame.Rect(10, 10, 80, 30)
water_button = pygame.Rect(100, 10, 80, 30)
soil_button = pygame.Rect(190, 10, 80, 30)
seed_button = pygame.Rect(280, 10, 80, 30)
selected_particle = SAND  # Default selection

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == SAND:
                pygame.draw.rect(screen, YELLOW, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == WATER:
                pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == SOIL_DRY:
                pygame.draw.rect(screen, BROWN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == SOIL_WET:
                pygame.draw.rect(screen, DARK_BROWN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == SEED:
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == GRASS:
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_buttons():
    pygame.draw.rect(screen, GRAY, sand_button)
    pygame.draw.rect(screen, GRAY, water_button)
    pygame.draw.rect(screen, GRAY, soil_button)
    pygame.draw.rect(screen, GRAY, seed_button)
    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Sand", True, WHITE), (sand_button.x + 20, sand_button.y + 5))
    screen.blit(font.render("Water", True, WHITE), (water_button.x + 20, water_button.y + 5))
    screen.blit(font.render("Soil", True, WHITE), (soil_button.x + 20, soil_button.y + 5))
    screen.blit(font.render("Seed", True, WHITE), (seed_button.x + 20, seed_button.y + 5))

def update_sand():
    for y in range(ROWS - 2, -1, -1):
        for x in range(COLS):
            if grid[y][x] == SAND:
                if grid[y + 1][x] == 0:  # Fall straight down
                    grid[y][x], grid[y + 1][x] = 0, SAND
                elif grid[y + 1][x] == WATER:  # Sink in water
                    grid[y][x], grid[y + 1][x] = WATER, SAND
                elif x > 0 and grid[y + 1][x - 1] == 0:  # Fall left
                    grid[y][x], grid[y + 1][x - 1] = 0, SAND
                elif x < COLS - 1 and grid[y + 1][x + 1] == 0:  # Fall right
                    grid[y][x], grid[y + 1][x + 1] = 0, SAND

def update_soil():
    for y in range(ROWS - 2, -1, -1):
        for x in range(COLS):
            if grid[y][x] == SOIL_DRY or grid[y][x] == SOIL_WET:
                if grid[y + 1][x] == 0:
                    grid[y][x], grid[y + 1][x] = 0, grid[y][x]

def update_water():
    for _ in range(2):  # Make water fall faster
        for y in range(ROWS - 2, -1, -1):
            for x in range(COLS):
                if grid[y][x] == WATER:
                    if grid[y + 1][x] == 0:  # Fall straight down
                        grid[y][x], grid[y + 1][x] = 0, WATER
                    elif grid[y + 1][x] == SOIL_DRY:
                        grid[y + 1][x] = SOIL_WET
                    else:
                        direction = random.choice([-1, 1])
                        if x + direction >= 0 and x + direction < COLS and grid[y][x + direction] == 0:
                            grid[y][x], grid[y][x + direction] = 0, WATER

def update_seeds():
    for y in range(ROWS - 1, -1, -1):
        for x in range(COLS):
            if grid[y][x] == SEED:
                if grid[y + 1][x] == 0:
                    grid[y][x], grid[y + 1][x] = 0, SEED
                elif grid[y + 1][x] == SOIL_WET:
                    grid[y][x] = GRASS

def add_particle():
    mx, my = pygame.mouse.get_pos()
    if my > 40 and 0 <= mx < WIDTH and 0 <= my < HEIGHT:
        grid[my // GRID_SIZE][mx // GRID_SIZE] = selected_particle

def main():
    global selected_particle
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sand_button.collidepoint(event.pos):
                    selected_particle = SAND
                elif water_button.collidepoint(event.pos):
                    selected_particle = WATER
                elif soil_button.collidepoint(event.pos):
                    selected_particle = SOIL_DRY
                elif seed_button.collidepoint(event.pos):
                    selected_particle = SEED
        
        if pygame.mouse.get_pressed()[0]:
            add_particle()
        
        update_sand()
        update_soil()
        update_water()
        update_seeds()
        draw_grid()
        draw_buttons()
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    main()
