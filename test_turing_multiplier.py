# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

# Unary multiplication machine
# Input format: a0b  where a and b are unary numbers
# Example: 110111  = 2 * 3

transitions = {
    # q0: find next unmarked 1 in first number
    ('q0', 'X'): ('q0', 'X', 'R'),
    ('q0', '1'): ('q1', 'X', 'R'),
    ('q0', '0'): ('q8', '0', 'R'),   # all first-number 1s processed

    # q1: move right to separator 0
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', 'X'): ('q1', 'X', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),

    # q2: scan second number for unmarked 1s
    ('q2', 'Y'): ('q2', 'Y', 'R'),
    ('q2', '1'): ('q3', 'Y', 'R'),
    ('q2', ''): ('q5', '', 'L'),

    # q3: move to end of tape
    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', 'Y'): ('q3', 'Y', 'R'),
    ('q3', '0'): ('q3', '0', 'R'),
    ('q3', ''): ('q4', '1', 'L'),

    # q4: return left to the marked Y we came from
    ('q4', '1'): ('q4', '1', 'L'),
    ('q4', '0'): ('q4', '0', 'L'),
    ('q4', 'Y'): ('q2', 'Y', 'R'),

    # q5: restore all Y markers back to 1
    ('q5', 'Y'): ('q5', '1', 'L'),
    ('q5', '1'): ('q5', '1', 'L'),
    ('q5', '0'): ('q5', '0', 'L'),
    ('q5', 'X'): ('q0', 'X', 'R'),

    # q8: cleanup phase after multiplication
    ('q8', '0'): ('q8', '0', 'R'),
    ('q8', '1'): ('q8', '1', 'R'),
    ('q8', ''): ('qa', '', 'R'),
}

if __name__ == "__main__":
    print_states(transitions)

    machine = TuringMachine(transitions)
    machine.enable_two_way_tape()

    def run(input_):
        print(f'Input: {input_}')
        result = machine.accepts(input_, step_limit=5000)
        print('Accepted' if result else 'Rejected')
        machine.debug(input_, step_limit=200)
        print()

    # 2 * 3 = 6
    run("110111")

    # 3 * 4 = 12
    run("11101111")

    # 0 * 4 = 0
    run("01111")
