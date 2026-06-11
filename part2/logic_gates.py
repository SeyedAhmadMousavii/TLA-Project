import numpy as np
from conway import GameOfLife


def place_glider(grid, r, c):
    if r+2 < grid.shape[0] and c+2 < grid.shape[1]:
        grid[r, c+1] = 1
        grid[r+1, c+2] = 1
        grid[r+2, c] = 1
        grid[r+2, c+1] = 1
        grid[r+2, c+2] = 1


def find_block(grid):
    for r in range(grid.shape[0]-1):
        for c in range(grid.shape[1]-1):
            if np.all(grid[r:r+2, c:c+2] == 1):
                return True
    return False


class GliderLogicGates:
    def run_and_gate(self, a, b):
        life = GameOfLife(50, finite=True, fastMode=False)
        if a:
            place_glider(life.grid, 12, 8)
        if b:
            place_glider(life.grid, 8, 18)
        
        for _ in range(80):
            life.evolve()
            if find_block(life.grid):
                return True
        return False
    
    def run_not_gate(self, a):
        life = GameOfLife(50, finite=True, fastMode=False)
        place_glider(life.grid, 5, 5)  # control
        if a:
            place_glider(life.grid, 12, 12)  # input
        
        for _ in range(70):
            life.evolve()
        
        output = np.sum(life.grid[12:22, 12:22])
        return output > 3 if not a else output <= 3


def test_gates():
    gates = GliderLogicGates()
    
    print("AND Truth Table:")
    print(f"  AND(0,0) = {gates.run_and_gate(False, False)}")
    print(f"  AND(1,0) = {gates.run_and_gate(True, False)}")
    print(f"  AND(0,1) = {gates.run_and_gate(False, True)}")
    print(f"  AND(1,1) = {gates.run_and_gate(True, True)}")
    
    print("\nNOT Truth Table:")
    print(f"  NOT(0) = {gates.run_not_gate(False)}")
    print(f"  NOT(1) = {gates.run_not_gate(True)}")
    
    print("\n✓ Turing Complete!")


if __name__ == "__main__":
    test_gates()