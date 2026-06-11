# -*- coding: utf-8 -*-
"""
Complete Glider test script to verify Game of Life implementation.
"""

import conway
from pygame_viewer import run_pygame_life


def test_glider_simple():
    """Test simple glider movement."""
    print("Running simple glider test...")
    life = conway.GameOfLife(N=64, finite=False, fastMode=False)
    life.insertGlider((0, 0))
    
    # Run without visualization to verify
    for step in range(20):
        life.evolve()
        if step % 4 == 0:
            grid = life.getStates()
            # Check if glider is still alive
            if np.sum(grid) == 0:
                print(f"ERROR: Glider died at step {step}")
                return False
    
    print("Simple glider test passed!")
    return True


def test_glider_gun():
    """Test Gosper Glider Gun (after fix)."""
    print("Testing Glider Gun (fixed version)...")
    life = conway.GameOfLife(N=100, finite=True, fastMode=True)
    life.insertGliderGun((0, 0))
    
    # Run for enough steps to see gliders emerge
    glider_count = 0
    for step in range(100):
        life.evolve()
        if step > 30 and step % 30 == 0:
            grid = life.getStates()
            # Count gliders (rough heuristic)
            count = np.sum(grid)
            if count > glider_count:
                glider_count = count
                print(f"Step {step}: {count} live cells")
    
    if glider_count > 50:
        print("Glider Gun test passed! Gun is producing gliders.")
        return True
    else:
        print("Warning: Low cell count - gun may not be working correctly")
        return False


def test_glider_visual():
    """Run visual test with pygame."""
    print("\nStarting visual test with pygame...")
    life = conway.GameOfLife(N=64, finite=False, fastMode=True)
    life.insertGlider((0, 0))
    
    run_pygame_life(
        life, 
        cell_scale=10, 
        fps=8, 
        max_frames=100, 
        title="Game of Life - Glider Test (c/4 diagonal movement)"
    )


if __name__ == "__main__":
    import numpy as np
    
    test_glider_simple()
    test_glider_gun()
    
    # Ask user if they want visual test
    response = input("\nRun visual test? (y/n): ")
    if response.lower() == 'y':
        test_glider_visual()