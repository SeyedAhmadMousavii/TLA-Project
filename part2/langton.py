# -*- coding: utf-8 -*-
"""
Langton's Ant Implementation.

This module implements Langton's Ant, a 2D Turing machine with simple rules
that produces complex emergent behavior including chaos and highways.
"""
import numpy as np


class LangtonsAnt:
    """
    [Part 2 - Langton's Ant]
    Langton's Ant implementation with multi-color state support.
    
    The ant follows these rules:
    - On a cell of color C: change to next_color, turn direction (R or L), move forward
    - Grid wraps around (toroidal boundaries)
    
    Directions: 0=Up (North), 1=Right (East), 2=Down (South), 3=Left (West)
    Turn: 'R' = clockwise (+1), 'L' = counter-clockwise (-1)
    """

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.
        
        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=np.int32)  # 0 = white/default, positive integers for other colors
        self.rules = rules
        self.max_color = max(rules.keys()) if rules else 0
        
        # Ant state
        self.ant_r, self.ant_c = ant_position
        self.direction = 0  # 0=Up, 1=Right, 2=Down, 3=Left
        
        # Direction vectors for movement
        self.dir_vectors = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def get_states(self):
        """
        Returns the current state grid of the cells.
        
        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).
        
        Returns:
            tuple: Current coordinates of the ant.
        """
        return (self.ant_r, self.ant_c)

    def step(self):
        """
        Perform a single simulation step following the ruleset.
        
        The ant:
        1. Reads the color of the current cell
        2. Updates the cell to the next color according to rules
        3. Turns left or right according to the rule
        4. Moves forward one cell (with toroidal wrapping)
        """
        # Get current cell color
        current_color = self.grid[self.ant_r, self.ant_c]
        
        # Apply rule - if color not in rules, default to R turn and stay same color
        if current_color in self.rules:
            next_color, turn = self.rules[current_color]
        else:
            # Default behavior: stay same color, turn right
            next_color = current_color
            turn = 'R'
        
        # Update cell color
        self.grid[self.ant_r, self.ant_c] = next_color
        
        # Turn the ant
        if turn == 'R':
            self.direction = (self.direction + 1) % 4
        elif turn == 'L':
            self.direction = (self.direction - 1) % 4
        
        # Move forward one cell (with toroidal wrapping)
        dr, dc = self.dir_vectors[self.direction]
        self.ant_r = (self.ant_r + dr) % self.N
        self.ant_c = (self.ant_c + dc) % self.N

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()