import numpy as np

class LangtonsAnt:
    def __init__(self, N, ant_position, rules):
        self.N = N
        self.grid = np.zeros((N, N), dtype=int)
        self.position = list(ant_position)
        self.rules = rules
        self.dir_idx = 0
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def get_states(self):
        return self.grid.copy()

    def get_current_position(self):
        return tuple(self.position)

    def step(self):
        r, c = self.position
        current_color = self.grid[r, c]
        if current_color in self.rules:
            next_color, turn = self.rules[current_color]
            if turn == 'R':
                self.dir_idx = (self.dir_idx + 1) % 4
            elif turn == 'L':
                self.dir_idx = (self.dir_idx - 1) % 4
            self.grid[r, c] = next_color
        else:
            self.grid[r, c] = (current_color + 1) % (max(self.rules.keys()) + 1)
            self.dir_idx = (self.dir_idx + 1) % 4
        dr, dc = self.directions[self.dir_idx]
        self.position[0] = (r + dr) % self.N
        self.position[1] = (c + dc) % self.N

    def update(self):
        self.step()