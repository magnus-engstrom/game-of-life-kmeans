import pygame
import numpy as np
import random
class Renderer:
    def __init__(self, grid_width, grid_height):
        pygame.init()
        self.scale = 4
        self.display=pygame.display.set_mode((grid_width*self.scale, grid_height*self.scale))
        self.clock = pygame.time.Clock()
        self.display.fill((5,5,5))

    def draw(self, grid):
        for row in grid:
            for cell in row:
                if cell.render:
                    rect = [cell.x*self.scale, cell.y*self.scale, self.scale, self.scale]
                    pygame.draw.rect(self.display, cell.genes, rect)
                    if random.randint(0,10) > 9:
                        pixel = [
                            cell.x*self.scale+random.randint(-1,self.scale+1), 
                            cell.y*self.scale+random.randint(-1,self.scale+1), 
                            1, 1]
                        pygame.draw.rect(self.display, cell.genes, pixel)
        pygame.display.update()
        self.clock.tick(60)