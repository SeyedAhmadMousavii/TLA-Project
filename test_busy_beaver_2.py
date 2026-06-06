# -*- coding: utf-8 -*-
from turing_machine import TuringMachine

bbeaver2 = TuringMachine(
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)

bbeaver3 = TuringMachine(
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'R'),
        ('b', '0'): ('c', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)

bbeaver4 = TuringMachine(
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('c', '1', 'R'),
        ('c', '0'): ('d', '1', 'L'),
        ('c', '1'): ('d', '1', 'R'),
        ('d', '0'): ('a', '1', 'R'),
        ('d', '1'): ('h', '1', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)

bbeaver5 = TuringMachine(
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('d', '1', 'R'),
        ('c', '0'): ('e', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
        ('d', '0'): ('c', '1', 'L'),
        ('d', '1'): ('e', '0', 'L'),
        ('e', '0'): ('a', '1', 'R'),
        ('e', '1'): ('b', '0', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)


def count_ones(machine, input_str, step_limit=100000):
    steps = list(machine.run(input_str))
    if not steps:
        return 0, 0
    
    final_action, config = steps[-1]
    if final_action != 'Accept':
        return len(steps), 0
    
    left = config['left_hand_side']
    symbol = config['symbol']
    right = config['right_hand_side']
    
    count = 0
    for s in left:
        if s == '1':
            count += 1
    if symbol == '1':
        count += 1
    for s in right:
        if s == '1':
            count += 1
    
    return len(steps), count


if __name__ == "__main__":
    for m in [bbeaver2, bbeaver3, bbeaver4, bbeaver5]:
        m.enable_two_way_tape()
    
    print("=" * 70)
    print("BUSY BEAVER PROBLEM - RESULTS")
    print("=" * 70)
    
    tests = [
        ("2-state", bbeaver2),
        ("3-state", bbeaver3),
        ("4-state", bbeaver4),
        ("5-state", bbeaver5),
    ]
    
    for name, machine in tests:
        print(f"\n{name} Busy Beaver:")
        print("-" * 40)
        
        input_tape = '0' * 10
        
        try:
            steps, ones = count_ones(machine, input_tape, step_limit=50000)
            print(f"  Steps executed: {steps}")
            print(f"  Number of 1s written: {ones}")
            
            machine.debug(input_tape, step_limit=min(50, steps))
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 70)
    print("KNOWN BB VALUES:")
    print("  BB(1) = 1")
    print("  BB(2) = 4")
    print("  BB(3) = 6")
    print("  BB(4) = 13")
    print("  BB(5) >= 4098")
    print("=" * 70)