import sys
from turing_machine import TuringMachine

beaver_programs = [
    {},
    
    {
        ('a', '0'): ('h', '1', 'R'),
        ('a', '1'): ('h', '1', 'R'),
    },
    
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },
    
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'R'),
        ('b', '0'): ('c', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
    },
    
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
    
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', '0'): ('c', '1', 'R'),
        ('b', '1'): ('d', '1', 'L'),
        ('c', '0'): ('e', '1', 'R'),
        ('c', '1'): ('f', '1', 'L'),
        ('d', '0'): ('a', '1', 'L'),
        ('d', '1'): ('e', '1', 'R'),
        ('e', '0'): ('f', '1', 'L'),
        ('e', '1'): ('h', '1', 'R'),
        ('f', '0'): ('d', '1', 'R'),
        ('f', '1'): ('b', '0', 'L'),
    },
]


def count_ones_on_tape(tm, input_str, step_limit=100000):
    steps = list(tm.run(input_str))
    if not steps:
        return 0
    
    final_action, config = steps[-1]
    if final_action != 'Accept':
        return 0
    
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
    
    return count


def busy_beaver(n):
    if n < 1 or n >= len(beaver_programs):
        print(f"n must be between 1 and {len(beaver_programs)-1}")
        return
    
    program = beaver_programs[n]
    
    print("=" * 60)
    print(f"Running Busy Beaver with {n} states")
    print("=" * 60)
    
    tm = TuringMachine(program, start_state='a', accept_state='h', reject_state='r', blank_symbol='0')
    tm.enable_two_way_tape()
    
    input_tape = '0' * 20
    
    print(f"Starting with blank tape...")
    
    try:
        steps_list = []
        for action, config in tm.run(input_tape):
            steps_list.append((action, config))
            if len(steps_list) % 1000 == 0:
                print(f"  ... {len(steps_list)} steps so far ...")
            if len(steps_list) > 100000:
                print(f"  Reached step limit 100000, stopping...")
                break
        
        if steps_list:
            final_action, final_config = steps_list[-1]
            ones_count = count_ones_on_tape(tm, input_tape, step_limit=200000)
            
            print(f"\n{'='*60}")
            print(f"RESULTS:")
            print(f"  Total steps taken: {len(steps_list)}")
            print(f"  Final action: {final_action}")
            print(f"  Number of 1s on tape: {ones_count}")
            print(f"{'='*60}")
            
            left = final_config['left_hand_side']
            symbol = final_config['symbol']
            right = final_config['right_hand_side']
            tape_str = ''.join(reversed(left)) + f"[{symbol}]" + ''.join(right)
            print(f"  Final tape (partial): {tape_str[:200]}")
    
    except Exception as e:
        print(f"Error during execution: {e}")


def usage():
    print("Usage: python busy_beaver.py [1|2|3|4|5|6]")
    print("Runs Busy Beaver problem for 1 to 6 states.")
    print("\nKnown results:")
    print("  BB(1) = 1")
    print("  BB(2) = 4")
    print("  BB(3) = 6")
    print("  BB(4) = 13")
    print("  BB(5) >= 4098")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        for i in range(1, 6):
            busy_beaver(i)
            print()
    else:
        n = int(sys.argv[1])
        if n < 1 or n > 6:
            print("n must be between 1 and 6")
            usage()
        busy_beaver(n)