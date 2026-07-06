import numpy as np
from scipy import signal

def parse_pattern(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
    if any('x =' in line for line in lines):
        return _parse_rle(content)
    else:
        return _parse_plaintext(content)

def _parse_rle(content):
    pattern = ''
    for line in content.splitlines():
        if line.startswith('#') or '=' in line or not line.strip():
            continue
        pattern += line.strip()
    rows = []
    i = 0
    current_row = []
    count = ''
    while i < len(pattern):
        if pattern[i].isdigit():
            count += pattern[i]
        elif pattern[i] in 'bo':
            num = int(count) if count else 1
            val = 1 if pattern[i] == 'o' else 0
            current_row.extend([val] * num)
            count = ''
        elif pattern[i] in '$!':
            rows.append(current_row)
            current_row = []
            if pattern[i] == '!':
                break
        i += 1
    if current_row:
        rows.append(current_row)
    max_w = max(len(r) for r in rows) if rows else 0
    grid = np.zeros((len(rows), max_w), dtype=np.uint8)
    for r_idx, row in enumerate(rows):
        grid[r_idx, :len(row)] = row
    live_cells = [(r, c) for r in range(grid.shape[0]) for c in range(grid.shape[1]) if grid[r, c] == 1]
    return grid.shape[1], grid.shape[0], live_cells

def _parse_plaintext(content):
    rows = []
    for line in content.splitlines():
        if line.startswith('!'):
            continue
        row = [1 if c in 'oO*' else 0 for c in line if c in '.boO*']
        if row:
            rows.append(row)
    if not rows:
        return 0, 0, []
    max_w = max(len(r) for r in rows)
    grid = np.zeros((len(rows), max_w), dtype=np.uint8)
    for r_idx, row in enumerate(rows):
        grid[r_idx, :len(row)] = row
    live_cells = [(r, c) for r in range(grid.shape[0]) for c in range(grid.shape[1]) if grid[r, c] == 1]
    return grid.shape[1], grid.shape[0], live_cells

class GameOfLife:
    def __init__(self, N=256, finite=False, fastMode=True):
        N = int(N)
        self.grid = np.zeros((N, N), dtype=np.uint8)
        self.neighborhood = np.ones((3, 3), dtype=np.uint8)
        self.neighborhood[1, 1] = 0
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N
        self.cols = N

    def getStates(self):
        return self.grid

    def getGrid(self):
        return self.getStates()

    def update_grid_fast(self, grid):
        if self.finite:
            count = signal.convolve2d(grid, self.neighborhood, mode='same', boundary='fill', fillvalue=0)
        else:
            count = signal.convolve2d(grid, self.neighborhood, mode='same', boundary='wrap')
        next_grid = np.zeros_like(grid)
        next_grid[(grid == 0) & (count == 3)] = 1
        next_grid[(grid == 1) & ((count == 2) | (count == 3))] = 1
        return next_grid

    def evolve(self):
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            new_grid = np.zeros_like(self.grid)
            for i in range(self.rows):
                for j in range(self.cols):
                    total = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni = i + di
                            nj = j + dj
                            if self.finite:
                                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                                    total += self.grid[ni, nj]
                            else:
                                total += self.grid[ni % self.rows, nj % self.cols]
                    if self.grid[i, j] == 1:
                        new_grid[i, j] = 1 if total in (2, 3) else 0
                    else:
                        new_grid[i, j] = 1 if total == 3 else 0
            self.grid = new_grid
        return self.grid

    def insertBlinker(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        self.grid[index[0] + 5, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2] = self.aliveValue

    def insertFromFile(self, filename, index=(0, 0)):
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            tr = index[0] + r
            tc = index[1] + c
            if 0 <= tr < self.rows and 0 <= tc < self.cols:
                self.grid[tr, tc] = self.aliveValue