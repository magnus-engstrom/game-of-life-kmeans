import pygame
import numpy as np
import random
class Renderer:
    def __init__(self, grid_width, grid_height, scale, bg_color):
        pygame.init()
        self.scale = scale
        self.display=pygame.display.set_mode((int(grid_width*self.scale), int(grid_height*self.scale)))
        self.clock = pygame.time.Clock()
        self.display.fill(bg_color)
        self.bg_color = bg_color
        for y in range(grid_height):
            for x in range(grid_width):
                rect = [x*self.scale, y*self.scale, self.scale, self.scale]
                pygame.draw.rect(self.display, bg_color * np.random.uniform(0.8,1.2), rect)
                pygame.draw.rect(self.display, bg_color * np.random.uniform(0.8,1.2), rect, 1)

    def draw(self, grid):
        for row in grid:
            for cell in row:
                if cell.render and np.sum(cell.genes) > 50:
                    if np.random.uniform(0.0,1.0) > 0.98:
                        pygame.draw.line(self.display, np.clip(np.rint(cell.genes), 0, 255), 
                        [cell.x*self.scale + np.random.uniform(0.0,self.scale), cell.y*self.scale + np.random.uniform(0.0,self.scale)], 
                        [cell.x*self.scale + np.random.uniform(0.0,self.scale), cell.y*self.scale + np.random.uniform(0.0,self.scale)], 
                        1)
        pygame.display.update()
        self.clock.tick(60)