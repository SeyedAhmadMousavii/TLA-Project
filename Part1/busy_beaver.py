import sys
from termcolor import colored


class Error(Exception):
    pass


class TuringMachine(object):
    def __init__(self, program, start, halt, init):
        self.program = program
        self.start = start
        self.halt = halt
        self.init = init
        self.tape = [self.init]
        self.pos = 0
        self.state = self.start
        self.set_tape_callback(None)
        self.tape_changed = 1
        self.movez = 0

    def run(self):
        tape_callback = self.get_tape_callback()
        while self.state != self.halt:
            if tape_callback:
                tape_callback(self.tape, self.tape_changed)

            lhs = self.get_lhs()
            rhs = self.get_rhs(lhs)

            new_state, new_symbol, move = rhs

            old_symbol = lhs[1]
            self.update_tape(old_symbol, new_symbol)
            self.update_state(new_state)
            self.move_head(move)

        if tape_callback:
            tape_callback(self.tape, self.tape_changed)

    def set_tape_callback(self, fn):
        self.tape_callback = fn

    def get_tape_callback(self):
        return self.tape_callback

    @property
    def moves(self):
        return self.movez

    def update_tape(self, old_symbol, new_symbol):
        if old_symbol != new_symbol:
            self.tape[self.pos] = new_symbol
            self.tape_changed += 1
        else:
            self.tape_changed = 0

    def update_state(self, state):
        self.state = state

    def get_lhs(self):
        under_cursor = self.tape[self.pos]
        lhs = self.state + under_cursor
        return lhs

    def get_rhs(self, lhs):
        if lhs not in self.program:
            raise Error('Could not find transition for state "%s".' % lhs)
        return self.program[lhs]

    def move_head(self, move):
        if move == 'l':
            self.pos -= 1
        elif move == 'r':
            self.pos += 1
        else:
            raise Error('Unknown move "%s". It can only be left or right.' % move)

        if self.pos < 0:
            self.tape.insert(0, self.init)
            self.pos = 0
        if self.pos >= len(self.tape):
            self.tape.append(self.init)

        self.movez += 1


beaver_programs = [
    {},

    # 1-state
    {'a0': ('h', '1', 'r')},

    # 2-state
    {
        'a0': ('b', '1', 'r'),
        'a1': ('b', '1', 'l'),
        'b0': ('a', '1', 'l'),
        'b1': ('h', '1', 'r'),
    },
    
    # =======================================================
    # 3-state with 14 steps
    # { 
    #     'a0': ('b', '1', 'r'),
    #     'a1': ('h', '1', 'r'),
    #     'b0': ('c', '0', 'r'),
    #     'b1': ('b', '1', 'r'),
    #     'c0': ('c', '1', 'l'),
    #     'c1': ('a', '1', 'l'),
    # },
    # =======================================================
    
    # 3-state with 21 steps
    {
        'a0': ('b', '1', 'r'),
        'a1': ('h', '1', 'r'),
        'b0': ('b', '1', 'l'),
        'b1': ('c', '0', 'r'),
        'c0': ('c', '1', 'l'),
        'c1': ('a', '1', 'l'),
    },

    # 4-state
    {
        'a0': ('b', '1', 'r'),
        'a1': ('b', '1', 'l'),
        'b0': ('a', '1', 'l'),
        'b1': ('c', '0', 'l'),
        'c0': ('h', '1', 'r'),
        'c1': ('d', '1', 'l'),
        'd0': ('d', '1', 'r'),
        'd1': ('a', '0', 'r'),
    },
]


def busy_beaver(n):
    def tape_callback(tape, tape_changed):
        if tape_changed:
            print(''.join(tape))

    program = beaver_programs[n]

    print(colored("Running Busy Beaver with %d states.", 'yellow') % n)
    tm = TuringMachine(program, 'a', 'h', '0')
    tm.set_tape_callback(tape_callback)
    tm.run()
    print(colored("Busy beaver finished in %d steps.", 'blue') % tm.moves)


def usage():
    print("Usage: %s [1|2|3|4]" % sys.argv[0])
    print("Runs Busy Beaver problem for 1 or 2 or 3 or 4 states.")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(colored("Enter the Number of States for Busy Beaver: ", 'red'))
        n = int(input())
    else:
        n = int(sys.argv[1])

    if n < 1 or n > 4:
        print("n must be between 1 and 4 inclusive")
        usage()

    busy_beaver(n)