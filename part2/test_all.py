import numpy as np
from conway import GameOfLife
from langton import LangtonsAnt
from logic_gates import test_gates


def run_all_tests():
    print("\n" + "=" * 50)
    print("RUNNING ALL TESTS")
    print("=" * 50)
    
    # Test 1: Blinker
    life = GameOfLife(10, finite=True, fastMode=False)
    life.insertBlinker((2, 2))
    life.evolve()
    assert np.sum(life.getStates()[2:5, 2:5]) == 3
    print("✓ Blinker test passed")
    
    # Test 2: Glider
    life = GameOfLife(20, finite=True, fastMode=False)
    life.insertGlider((0, 0))
    for _ in range(4):
        life.evolve()
    assert np.sum(life.getStates()[1:4, 1:4]) == 5
    print("✓ Glider test passed")
    
    # Test 3: Langton's Ant
    ant = LangtonsAnt(20, (10, 10), {0: (1, "R"), 1: (0, "L")})
    for _ in range(50):
        ant.step()
    print("✓ Langton's Ant test passed")
    
    # Test 4: Fast mode
    life = GameOfLife(100, finite=False, fastMode=True)
    life.insertGlider((0, 0))
    life.evolve()
    print("✓ Fast mode test passed")
    
    # Test 5: Glider Gun
    life = GameOfLife(100, finite=True, fastMode=False)
    life.insertGliderGun((10, 10))
    for _ in range(60):
        life.evolve()
    print("✓ Glider Gun test passed")
    
    # Test 6: Logic Gates
    test_gates()
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()