import sys
from turing_machine import TuringMachine

beaver_programs = [
    {},

    # BB(1) = 1 one, 1 step
    {
        ('a', '0'): ('h', '1', 'R'),
    },

    # BB(2) = 4 ones, 6 steps
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },

    # BB(3) = 6 ones, 21 steps
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('h', '1', 'R'),
        ('b', '0'): ('c', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '1', 'L'),
        ('c', '1'): ('b', '1', 'L'),
    },

    # BB(4) = 13 ones, 107 steps
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

    # BB(5) = 4098 ones, 47,176,870 steps
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
]


def count_ones(config):
    count = 0

    for s in config['left_hand_side']:
        if s == '1':
            count += 1

    if config['symbol'] == '1':
        count += 1

    for s in config['right_hand_side']:
        if s == '1':
            count += 1

    return count


def busy_beaver(n):
    if n < 1 or n >= len(beaver_programs):
        print(f"n must be between 1 and {len(beaver_programs)-1}")
        return

    program = beaver_programs[n]

    print("=" * 60)
    print(f"Running Busy Beaver with {n} states.")
    print("=" * 60)

    tm = TuringMachine(
        program,
        start_state='a',
        accept_state='h',
        reject_state='r',
        blank_symbol='0'
    )

    tm.enable_two_way_tape()

    steps = 0
    final_action = None
    final_config = None

    step_limits = {
        1: 10,
        2: 20,
        3: 50,
        4: 200,
        5: 100000
    }

    step_limit = step_limits.get(n, 10000)

    print(f"Step limit: {step_limit}")

    try:
        for action, config in tm.run('0' * 20):

            final_action = action
            final_config = config

            if action is None:
                steps += 1

            if steps >= step_limit:
                print(f"\nStep limit {step_limit} reached")
                break

            if action in ('Accept', 'Reject'):
                break

    except KeyboardInterrupt:
        print(f"\nInterrupted at step {steps}")

    print(f"\nSteps executed: {steps}")
    print(f"Final action: {final_action}")

    if final_config:
        ones = count_ones(final_config)
        print(f"Number of 1s on tape: {ones}")
    else:
        ones = 0

    expected = {
        1: 1,
        2: 4,
        3: 6,
        4: 13,
        5: 4098
    }

    expected_steps = {
        1: 1,
        2: 6,
        3: 21,
        4: 107,
        5: 47176870
    }

    if n in expected:
        if (
            final_action == 'Accept'
            and ones == expected[n]
            and steps == expected_steps[n]
        ):
            print(
                f"\n✓ SUCCESS! "
                f"BB({n}) = {expected[n]} ones "
                f"in {expected_steps[n]} steps"
            )
        else:
            print(
                f"\n✗ Expected BB({n}) = "
                f"{expected[n]} ones in "
                f"{expected_steps[n]} steps"
            )
            print(
                f"  Got: {ones} ones "
                f"in {steps} steps"
            )

    print("=" * 60)


def usage():
    print(f"Usage: {sys.argv[0]} [1|2|3|4|5]")
    print("Runs Busy Beaver problem for 1, 2, 3, 4, or 5 states.")

    print("\nKnown BB values:")
    print("  BB(1) = 1 (1 step)")
    print("  BB(2) = 4 (6 steps)")
    print("  BB(3) = 6 (21 steps)")
    print("  BB(4) = 13 (107 steps)")
    print("  BB(5) = 4098 (47,176,870 steps)")

    sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()

    n = int(sys.argv[1])

    if n < 1 or n > 5:
        print("n must be between 1 and 5")
        usage()

    busy_beaver(n)