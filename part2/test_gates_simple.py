# -*- coding: utf-8 -*-
"""
Simple test for logic gates with visual output.
"""

import numpy as np
from conway import GameOfLife


def create_and_gate_demo():
    """Create a simple AND gate demonstration."""
    print("\n" + "=" * 60)
    print("AND GATE DEMONSTRATION")
    print("=" * 60)
    
    life = GameOfLife(40, finite=True, fastMode=False)
    
    # Place two gliders that will collide
    # Glider 1: moving right/down
    life.grid[0, 1] = 1
    life.grid[1, 2] = 1
    life.grid[2, 0] = 1
    life.grid[2, 1] = 1
    life.grid[2, 2] = 1
    
    # Glider 2: moving down/left from different position
    life.grid[8, 10] = 1
    life.grid[9, 11] = 1
    life.grid[10, 9] = 1
    life.grid[10, 10] = 1
    life.grid[10, 11] = 1
    
    print("Initial live cells:", np.sum(life.getStates()))
    
    # Run simulation and track collisions
    for step in range(80):
        life.evolve()
        if step % 10 == 0:
            live = np.sum(life.getStates())
            print(f"  Step {step}: {live} live cells")
    
    grid = life.getStates()
    
    # Check for 2x2 blocks (stable patterns from collision)
    blocks_found = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if np.all(grid[r:r+2, c:c+2] == 1):
                blocks_found.append((r, c))
    
    if blocks_found:
        print(f"\n✓ Found {len(blocks_found)} 2x2 blocks at: {blocks_found}")
        print("  This simulates AND gate output (both inputs = 1)")
    else:
        print("\n✗ No 2x2 blocks found")


def create_not_gate_demo():
    """Create a simple NOT gate demonstration."""
    print("\n" + "=" * 60)
    print("NOT GATE DEMONSTRATION")
    print("=" * 60)
    
    # Case 1: Input = 0 (should have output)
    print("\nCase 1: Input = 0 (Control glider alone)")
    life1 = GameOfLife(40, finite=True, fastMode=False)
    
    # Control glider only
    life1.grid[3, 2] = 1
    life1.grid[4, 3] = 1
    life1.grid[5, 1] = 1
    life1.grid[5, 2] = 1
    life1.grid[5, 3] = 1
    
    for step in range(50):
        life1.evolve()
    
    grid1 = life1.getStates()
    output1 = np.sum(grid1[10:20, 10:20])
    print(f"  Output region live cells: {output1}")
    
    # Case 2: Input = 1 (should have annihilation, no output)
    print("\nCase 2: Input = 1 (Control + Input gliders collide)")
    life2 = GameOfLife(40, finite=True, fastMode=False)
    
    # Control glider
    life2.grid[3, 2] = 1
    life2.grid[4, 3] = 1
    life2.grid[5, 1] = 1
    life2.grid[5, 2] = 1
    life2.grid[5, 3] = 1
    
    # Input glider (will collide with control)
    life2.grid[6, 8] = 1
    life2.grid[7, 9] = 1
    life2.grid[8, 7] = 1
    life2.grid[8, 8] = 1
    life2.grid[8, 9] = 1
    
    for step in range(50):
        life2.evolve()
    
    grid2 = life2.getStates()
    output2 = np.sum(grid2[10:20, 10:20])
    print(f"  Output region live cells: {output2}")
    
    if output1 > output2:
        print("\n✓ NOT gate behavior: output when input=0, no output when input=1")
    else:
        print("\n✗ NOT gate not behaving as expected")


def create_glider_collision():
    """Create and show glider collision."""
    print("\n" + "=" * 60)
    print("GLIDER COLLISION DEMONSTRATION")
    print("=" * 60)
    
    life = GameOfLife(30, finite=True, fastMode=False)
    
    # Create two gliders heading toward each other
    # Glider A (from top-left)
    life.grid[0, 1] = 1
    life.grid[1, 2] = 1
    life.grid[2, 0] = 1
    life.grid[2, 1] = 1
    life.grid[2, 2] = 1
    
    # Glider B (from bottom-right)
    life.grid[25, 26] = 1
    life.grid[26, 27] = 1
    life.grid[27, 25] = 1
    life.grid[27, 26] = 1
    life.grid[27, 27] = 1
    
    print("Two gliders moving toward each other")
    
    # Run until collision
    for step in range(60):
        life.evolve()
        live = np.sum(life.getStates())
        if step % 10 == 0:
            print(f"  Step {step}: {live} live cells")
    
    grid = life.getStates()
    
    # Check what happened
    if np.sum(grid) > 0:
        print(f"\n  Final live cells: {np.sum(grid)}")
        
        # Look for blocks
        blocks = 0
        for r in range(grid.shape[0] - 1):
            for c in range(grid.shape[1] - 1):
                if np.all(grid[r:r+2, c:c+2] == 1):
                    blocks += 1
        
        if blocks > 0:
            print(f"  Found {blocks} stable blocks after collision")
            print("  ✓ This demonstrates how gliders can create stable patterns")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMPLE LOGIC GATES TESTS")
    print("=" * 60)
    
    create_glider_collision()
    create_and_gate_demo()
    create_not_gate_demo()
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)
    print("\nNote: For full logic gate tests, install scipy and run:")
    print("  python logic_gates.py")