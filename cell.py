import numpy as np

class Cell:
    def __init__(self, x, y, active):
        self.x = x
        self.y = y
        self.active = active
        self.genes = (0, 0, 0)
        self.render = True
        self.age = 0
    
    def step(self, neighbors):
        self.age += 1
        self.render = True
        if neighbors['count'] == 3 and self.age < 50:
            if not self.active:
                self.active = True
                self.age = 1
                self.genes = np.rint(np.mean(np.stack(neighbors['genes'], axis=-1), axis=1))
                if np.random.uniform(0,1) > 0.96:
                    self.genes = np.clip(self.genes * np.random.default_rng().uniform(0.5,1.5,3), 0, 255)
            return
        if neighbors['count'] == 2 and self.active and self.age < 50:
            if np.sum(self.genes) < 250:
                self.genes = np.clip(self.genes * 1.01, 0, 255)
            return
        # if np.sum(self.genes) > 200:
        #     self.genes = self.genes / (1+np.random.uniform(0,0.5))
        if np.sum(self.genes) > 10 and np.sum(self.genes) < 250:
            self.genes = np.clip(self.genes * (1+np.random.uniform(0,0.2)), 0, 255)
        else:
            self.render = False
        self.active = False
        self.age = 1