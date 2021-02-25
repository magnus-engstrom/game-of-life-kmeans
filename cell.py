import numpy as np
import random

class Cell:
    def __init__(self, x, y, active, mutation_propability, start_color):
        self.x = x
        self.y = y
        self.active = active
        self.genes = start_color * 0.2
        self.render = True
        self.age = 0
        self.mutation_propability = mutation_propability
    
    def step(self, neighbors):
        self.render = True
        if neighbors['count'] == 3 and self.age < 10:
            if not self.active:
                self.active = True
                self.age = 1
                new_genes = []
                for r in neighbors['genes']:
                    if np.sum(r) > 20.0 and np.sum(r) < 240*3:
                        new_genes.append(r * np.random.uniform(0.94,1.05))
                if len(new_genes) > 0:
                    self.genes = np.mean(np.array(new_genes),  axis=0) * 0.95 + np.array(self.genes) * 0.05
                    self.genes = np.clip(self.genes, 0, 240)
            return
        if neighbors['count'] == 2 and self.active and self.age < 10:
            self.age += 1
            if random.randint(0,10) > 9:
                self.genes = np.array(self.genes) * np.random.uniform(0.8,1.1)
            if np.random.uniform(0.0,1.0) <= self.mutation_propability:
                self.genes *= 1.16
                self.genes *= np.random.default_rng().uniform(0.93,1.1,3)
            return
        if np.sum(self.genes) > 250 and self.active:
            self.genes *= np.random.uniform(0.8,1.1)
            self.genes = np.clip(self.genes, 0, 240)
        self.active = False
        self.age = 1