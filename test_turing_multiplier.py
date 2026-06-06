# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {
    ('q0', '1'): ('q1', 'x', 'R'),
    ('q0', '0'): ('qh', '0', 'R'),
    
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),
    
    ('q2', '1'): ('q2', '1', 'R'),
    ('q2', ''): ('q3', '', 'L'),
    
    ('q3', '1'): ('q4', 'y', 'L'),
    ('q3', '0'): ('q0', '0', 'L'),
    
    ('q4', '1'): ('q4', '1', 'L'),
    ('q4', '0'): ('q4', '0', 'L'),
    ('q4', 'x'): ('q4', 'x', 'L'),
    ('q4', ''): ('q5', '', 'R'),
    
    ('q5', 'x'): ('q2', 'x', 'R'),
    ('q5', 'y'): ('q5', 'y', 'R'),
    ('q5', '1'): ('q5', '1', 'R'),
    ('q5', '0'): ('q5', '0', 'R'),
    
    ('q6', 'y'): ('q6', '1', 'R'),
    
    ('qh', 'x'): ('qh', '', 'R'),
    ('qh', '1'): ('qh', '1', 'R'),
    ('qh', 'y'): ('qh', '1', 'R'),
    ('qh', ''): ('qa', '', 'R'),
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:", w)
        result = machine.accepts(w, step_limit=500)
        print("Accepted" if result else "Rejected")
        machine.debug(w, step_limit=500)
        print()

    run("110111")
    run("11101111")
    run("01111")