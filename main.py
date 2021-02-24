import random
import os
import sys
from cell import Cell
from renderer import Renderer
import pygame
import time
import numpy as np
import math
from sklearn.cluster import KMeans

WIDTH = int(4*35.0)
HEIGHT = int(2.5*35.0)
CELL_SIZE = 5
N_COLORS = 1 #np.random.randint(1, 4)
VOID_CLUSTERS = 10 #np.random.randint(1, 41)
CLUSTER_DENSITY = 0.3 #np.random.uniform(0.3,0.55)
NOISE_CELLS = 0.05 #np.random.uniform(0.0,0.01)
MUTATION_PROBABILITY = np.random.uniform(0.05,0.3)
COLOR_SEEDS = np.array([[1.0, 1.0, 1.0]])
BG_COLOR = np.random.default_rng().uniform(5.0,30.0,3) * COLOR_SEEDS[np.random.randint(0, COLOR_SEEDS.shape[0])]
MAX_GENREATIONS = 500
grid = []
generation = 0

print("DENSITY", CLUSTER_DENSITY)
print("MUTATION_PROBABILITY", MUTATION_PROBABILITY)
print("NOISE_CELLS", NOISE_CELLS)

grid = []
colors = []
for _ in range(N_COLORS):
    colors.append(np.random.default_rng().uniform(20.0,125.0,3) * COLOR_SEEDS[np.random.randint(0, COLOR_SEEDS.shape[0])])
    #colors.append([70.0, 30.0, 0.0])
for _ in range(VOID_CLUSTERS):
    colors.append(np.array([0, 0, 0]))


X_train = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        active = False
        if np.random.uniform(0,1.0) <= CLUSTER_DENSITY:
            active = True
        if active:
            X_train.append(np.array([x, y]) / (WIDTH, HEIGHT))
        row.append(Cell(x, y, active, MUTATION_PROBABILITY, BG_COLOR))
    grid.append(row)

kmeans = KMeans(n_clusters=len(colors)).fit(X_train)

grid_renderer = Renderer(WIDTH, HEIGHT, CELL_SIZE, BG_COLOR)

if __name__ == "__main__":
    done = False
    while not done:
        generation += 1
        if generation % 100 == 0:
            print(generation)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if pygame.key.get_focused():
                    if event.key == pygame.K_r:
                        generation = MAX_GENREATIONS
        neighbors_grid = []
        if generation <= MAX_GENREATIONS:
            for y in range(HEIGHT):
                neighbors_row = []
                for x in range(WIDTH):
                    neighbors = 0
                    genes = []
                    if not x >= WIDTH-1 and grid[y][x+1].active:
                        neighbors += 1
                        genes.append(grid[y][x+1].genes)
                    if not x >= WIDTH-1 and not y == 0 and grid[y-1][x+1].active:
                        neighbors += 1
                        genes.append(grid[y-1][x+1].genes)
                    if not x >= WIDTH-1 and not y >= HEIGHT-1 and grid[y+1][x+1].active:
                        neighbors += 1
                        genes.append(grid[y+1][x+1].genes)
                    if x > 0 and grid[y][x-1].active:
                        neighbors += 1
                        genes.append(grid[y][x-1].genes)
                    if x > 0 and not y == 0 and grid[y-1][x-1].active:
                        neighbors += 1
                        genes.append(grid[y-1][x-1].genes)
                    if x > 0 and y < HEIGHT-1 and grid[y+1][x-1].active:
                        neighbors += 1
                        genes.append(grid[y+1][x-1].genes)
                    if y < HEIGHT-1 and grid[y+1][x].active:
                        neighbors += 1
                        genes.append(grid[y+1][x].genes)
                    if y > 0 and grid[y-1][x].active:
                        neighbors += 1
                        genes.append(grid[y-1][x].genes)
                    neighbors_row.append({
                        "count": neighbors,
                        "genes": genes
                    })                    
                neighbors_grid.append(neighbors_row)

            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if grid[y][x].age == 0 and grid[y][x].active:
                        grid[y][x].genes = colors[kmeans.predict([np.array([x, y]) / (WIDTH, HEIGHT)])[0]] * np.random.default_rng().uniform(0.95,1,3)
                        grid[y][x].genes = np.clip(grid[y][x].genes, 0, 255)
 
                        if np.sum(grid[y][x].genes) < 20:
                            grid[y][x].active = False
                        else:
                            if np.random.uniform(0,1.0) <= NOISE_CELLS:
                                grid[y][x].genes * np.random.default_rng().uniform(0.5,1.5,3) * COLOR_SEEDS[np.random.randint(0, COLOR_SEEDS.shape[0])]
                    grid[y][x].step(neighbors_grid[y][x])

            grid_renderer.draw(grid)
        if generation > MAX_GENREATIONS:
            time.sleep(5)
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
    pygame.quit()