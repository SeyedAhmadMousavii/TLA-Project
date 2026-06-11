"""
The Game of Life (GoL) module named in honour of John Conway
"""
import numpy as np

try:
    from scipy import signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not installed. Fast convolution mode will not be available.")


def parse_pattern(filepath):
    """Parse RLE or Plaintext pattern files."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # RLE format
    if content.strip().startswith('x='):
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        header = lines[0]
        
        import re
        x_match = re.search(r'x\s*=\s*(\d+)', header)
        y_match = re.search(r'y\s*=\s*(\d+)', header)
        width = int(x_match.group(1)) if x_match else 100
        height = int(y_match.group(1)) if y_match else 100
        
        data = ''.join(lines[1:])
        if '!' in data:
            data = data.split('!')[0]
        data = ''.join(data.split())
        
        live_cells = []
        row, col = 0, 0
        i = 0
        
        while i < len(data):
            ch = data[i]
            count = 1
            if ch.isdigit():
                j = i
                while j < len(data) and data[j].isdigit():
                    j += 1
                count = int(data[i:j])
                i = j
                ch = data[i] if i < len(data) else ''
            
            if ch == 'b':
                col += count
            elif ch == 'o':
                for _ in range(count):
                    live_cells.append((row, col))
                    col += 1
            elif ch == '$':
                row += count
                col = 0
            i += 1
    else:
        # Plaintext format
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('!'):
                lines.append(line)
        
        height = len(lines)
        width = max(len(l) for l in lines) if lines else 0
        live_cells = []
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch in ['O', 'o']:
                    live_cells.append((r, c))
    
    return width, height, live_cells


class GameOfLife:
    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint8)
        self.finite = finite
        self.fastMode = fastMode and SCIPY_AVAILABLE
        self.aliveValue = 1
        self.rows = self.cols = N

    def getStates(self):
        return self.grid

    def update_grid_fast(self, grid):
        kernel = np.ones((3, 3), np.uint8)
        kernel[1, 1] = 0
        if self.finite:
            neighbor_count = signal.convolve2d(grid, kernel, mode='same', boundary='fill', fillvalue=0)
        else:
            neighbor_count = signal.convolve2d(grid, kernel, mode='same', boundary='wrap')
        
        new_grid = np.zeros_like(grid)
        birth = (grid == 0) & (neighbor_count == 3)
        survive = (grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))
        new_grid[birth | survive] = 1
        return new_grid

    def evolve(self):
        if self.fastMode and SCIPY_AVAILABLE:
            self.grid = self.update_grid_fast(self.grid)
        else:
            new_grid = np.zeros((self.rows, self.cols), np.uint8)
            for r in range(self.rows):
                for c in range(self.cols):
                    neighbors = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if self.finite:
                                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                    neighbors += self.grid[nr, nc]
                            else:
                                neighbors += self.grid[nr % self.rows, nc % self.cols]
                    
                    if self.grid[r, c] == 1:
                        if neighbors == 2 or neighbors == 3:
                            new_grid[r, c] = 1
                    else:
                        if neighbors == 3:
                            new_grid[r, c] = 1
            self.grid = new_grid

    def insertBlinker(self, idx):
        r, c = idx
        self.grid[r, c+1] = 1
        self.grid[r+1, c+1] = 1
        self.grid[r+2, c+1] = 1

    def insertGlider(self, idx):
        r, c = idx
        self.grid[r, c+1] = 1
        self.grid[r+1, c+2] = 1
        self.grid[r+2, c] = 1
        self.grid[r+2, c+1] = 1
        self.grid[r+2, c+2] = 1

    def insertGliderGun(self, idx):
        r, c = idx
        # Fixed left block
        self.grid[r+5, c+1] = 1
        self.grid[r+5, c+2] = 1
        self.grid[r+6, c+1] = 1
        self.grid[r+6, c+2] = 1
        
        # Rest of the gun
        self.grid[r+1, c+26] = 1
        self.grid[r+2, c+24] = 1
        self.grid[r+2, c+26] = 1
        self.grid[r+3, c+14] = 1
        self.grid[r+3, c+15] = 1
        self.grid[r+3, c+22] = 1
        self.grid[r+3, c+23] = 1
        self.grid[r+3, c+36] = 1
        self.grid[r+3, c+37] = 1
        self.grid[r+4, c+13] = 1
        self.grid[r+4, c+17] = 1
        self.grid[r+4, c+22] = 1
        self.grid[r+4, c+23] = 1
        self.grid[r+4, c+36] = 1
        self.grid[r+4, c+37] = 1
        self.grid[r+5, c+12] = 1
        self.grid[r+5, c+18] = 1
        self.grid[r+5, c+22] = 1
        self.grid[r+5, c+23] = 1
        self.grid[r+6, c+12] = 1
        self.grid[r+6, c+16] = 1
        self.grid[r+6, c+18] = 1
        self.grid[r+6, c+19] = 1
        self.grid[r+6, c+24] = 1
        self.grid[r+6, c+26] = 1
        self.grid[r+7, c+12] = 1
        self.grid[r+7, c+18] = 1
        self.grid[r+7, c+26] = 1
        self.grid[r+8, c+13] = 1
        self.grid[r+8, c+17] = 1
        self.grid[r+9, c+14] = 1
        self.grid[r+9, c+15] = 1

    def insertFromFile(self, filename, idx=(0, 0)):
        w, h, cells = parse_pattern(filename)
        for r, c in cells:
            tr, tc = idx[0] + r, idx[1] + c
            if 0 <= tr < self.rows and 0 <= tc < self.cols:
                self.grid[tr, tc] = 1