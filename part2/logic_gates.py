import numpy as np
from conway import GameOfLife

class GliderLogicGates:
    def setup_and_gate(self, grid_size=60, input_a_present=False, input_b_present=False):
        life = GameOfLife(N=grid_size, finite=False, fastMode=True)
        if input_a_present:
            life.insertGlider((15, 10))
        if input_b_present:
            life.insertGlider((10, 25))
        return life

    def run_and_gate(self, input_a_present, input_b_present):
        life = self.setup_and_gate(input_a_present, input_b_present)
        for _ in range(150):
            life.evolve()
        output_grid = life.getStates()
        return np.sum(output_grid[30:40, 30:40]) > 3

    def setup_not_gate(self, grid_size=70, input_a_present=False):
        life = GameOfLife(N=grid_size, finite=False, fastMode=True)
        life.insertGlider((10, 10))
        if input_a_present:
            life.insertGlider((25, 25))
        return life

    def run_not_gate(self, input_a_present):
        life = self.setup_not_gate(input_a_present)
        for _ in range(180):
            life.evolve()
        output_grid = life.getStates()
        return np.sum(output_grid[40:50, 40:50]) > 4

if __name__ == "__main__":
    gates = GliderLogicGates()
    print("AND(0,0):", gates.run_and_gate(False, False))
    print("AND(1,0):", gates.run_and_gate(True, False))
    print("AND(0,1):", gates.run_and_gate(False, True))
    print("AND(1,1):", gates.run_and_gate(True, True))
    print("NOT(0):", gates.run_not_gate(False))
    print("NOT(1):", gates.run_not_gate(True))