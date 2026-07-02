import sys
from turing_machine import TuringMachine


beaver_programs = [
    {},

    # BB(1) = 1 one, 1 step
    {
        ('a', ''): ('h', '1', 'R'),
    },

    # BB(2) = 4 ones, 6 steps
    {
        ('a', ''): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', ''): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },

    # BB(3) = 6 ones, 21 steps
    {
        ('a', ''): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'R'),
        ('b', ''): ('c', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', ''): ('a', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
    },

    # BB(4) = 13 ones, 107 steps
    {
        ('a', ''): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', ''): ('a', '1', 'L'),
        ('b', '1'): ('c', '1', 'R'),
        ('c', ''): ('d', '1', 'L'),
        ('c', '1'): ('d', '1', 'R'),
        ('d', ''): ('a', '1', 'R'),
        ('d', '1'): ('h', '1', 'R'),
    },

    # BB(5) approximate champion
    {
        ('a', ''): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', ''): ('a', '1', 'L'),
        ('b', '1'): ('d', '1', 'R'),
        ('c', ''): ('e', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
        ('d', ''): ('c', '1', 'L'),
        ('d', '1'): ('e', '', 'L'),
        ('e', ''): ('a', '1', 'R'),
        ('e', '1'): ('b', '', 'R'),
    },
]


def busy_beaver(n):
    def tape_callback(tape, tape_changed):
        if tape_changed:
            print(''.join(tape))

    program = beaver_programs[n]

    print("Running Busy Beaver with %d states." % n)
    tm = TuringMachine(program, 'a', 'h', '0')
    tm.set_tape_callback(tape_callback)
    tm.run()
    print("Busy beaver finished in %d steps." % tm.moves)


def usage():
    print("Usage: %s [1|2|3|4|5|6]" % sys.argv[0])
    print("Runs Busy Beaver problem for 1 or 2 or 3 or 4 or 5 or 6 states.")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    n = int(sys.argv[1])
    if n < 1 or n > 6:
        print("n must be between 1 and 6 inclusive")
        usage()
    busy_beaver(n)