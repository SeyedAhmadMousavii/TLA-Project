# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {
    # Find first 1 of first number and mark it as X
    ('q0', '1'): ('q1', 'X', 'R'),
    ('q0', '0'): ('q9', '0', 'R'),
    ('q0', 'X'): ('q0', 'X', 'R'),
    
    # Move right to find separator
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),
    
    # Move right through second number
    ('q2', '1'): ('q3', 'Y', 'R'),
    ('q2', '0'): ('q5', '0', 'L'),
    ('q2', ''): ('q5', '', 'L'),
    ('q2', 'Y'): ('q2', 'Y', 'R'),
    
    # Move to end of tape to write a copy of 1
    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', '0'): ('q3', '0', 'R'),
    ('q3', 'Y'): ('q3', 'Y', 'R'),
    ('q3', ''): ('q4', '1', 'L'),
    
    # Move left back to find next Y
    ('q4', '1'): ('q4', '1', 'L'),
    ('q4', '0'): ('q4', '0', 'L'),
    ('q4', 'Y'): ('q2', 'Y', 'R'),
    
    # Move left back to find X
    ('q5', '1'): ('q5', '1', 'L'),
    ('q5', '0'): ('q5', '0', 'L'),
    ('q5', 'Y'): ('q6', '1', 'L'),
    ('q5', 'X'): ('q7', 'X', 'R'),
    ('q5', ''): ('q8', '', 'R'),
    
    # Continue to next X or finish
    ('q6', 'Y'): ('q6', '1', 'L'),
    ('q6', 'X'): ('q7', 'X', 'R'),
    ('q6', ''): ('q8', '', 'R'),
    
    # Move right to find next X
    ('q7', 'X'): ('q7', 'X', 'R'),
    ('q7', '1'): ('q1', 'X', 'R'),
    ('q7', '0'): ('q8', '0', 'R'),
    
    # Clean up phase
    ('q8', 'Y'): ('q8', '1', 'R'),
    ('q8', '1'): ('q8', '1', 'R'),
    ('q8', '0'): ('q8', '0', 'R'),
    ('q8', 'X'): ('q8', '', 'R'),
    ('q8', ''): ('qa', '', 'R'),
    
    ('q9', 'X'): ('q9', '', 'R'),
    ('q9', '1'): ('q9', '1', 'R'),
    ('q9', ''): ('qa', '', 'R'),
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)
    machine.enable_two_way_tape()

    def run(input_):
        print(f'Input: {input_}')
        result = machine.accepts(input_, step_limit=500)
        print('Accepted' if result else 'Rejected')
        machine.debug(input_, step_limit=120)
        print()

    run("110111")
    run("11101111")
    run("01111")