import random
from cell import Cell
from renderer import Renderer
import pygame
import time
import numpy as np
import math
from sklearn.cluster import KMeans

WIDTH = 160
HEIGHT = 90
generation = 0
grid = []

colors = [
    # np.array([255, 43, 43]),
    # np.array([255, 210, 0]),
    np.array([65, 10, 10]),
    np.array([10, 10, 65]),
    np.array([10, 65, 10]),
    np.array([100, 100, 100]),
    # np.array([255, 43, 255]),
    # np.array([255, 255, 0]), 
    # np.array([100, 255, 100]), 
    # np.array([255, 255, 255]),
    
    # np.array([154, 3, 30]),
    # np.array([251, 139, 36]),
    # np.array([227, 100, 20]),
    #np.array([]),
    #np.array([255, 0, 255]),
    # np.array([255, 0, 255]),
    # np.array([0, 255, 150]),
    # np.array([150, 0, 255]),
    # np.array([255, 0, 150]),
]

X_train = []

for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        active = random.choice([True, False, False])
        if y < int(HEIGHT / 4) or y > int(HEIGHT*0.75):
            active = False
        if y > int(HEIGHT / 2) and y < int(HEIGHT*0.66):
            active = False
        if active:
            X_train.append(np.array([x, y]) / (WIDTH, HEIGHT))
        row.append(Cell(x, y, active))
    grid.append(row)

kmeans = KMeans(n_clusters=len(colors)).fit(X_train)

grid_renderer = Renderer(WIDTH, HEIGHT)

if __name__ == "__main__":
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
        neighbors_grid = []
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
                    grid[y][x].genes = colors[kmeans.predict([np.array([x, y]) / (WIDTH, HEIGHT)])[0]] * np.random.default_rng().uniform(0.5,1,3)
                grid[y][x].step(neighbors_grid[y][x])

        grid_renderer.draw(grid)
        generation += 1

    pygame.quit()