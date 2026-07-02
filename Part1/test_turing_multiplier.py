# -*- coding: utf-8 -*-
from turing_machine import TuringMachine

def print_states(transitions):
    """Print all states in the transitions."""
    states = set()
    for (state, sym), (nstate, _, _) in transitions.items():
        states.add(state)
        states.add(nstate)
    print("States:", sorted([s for s in states if s != 'qa']))

#create the Turing machine
transitions = {
    ('q0', '1'): ('q2','#','R'),
    ('q0', '0'): ('qa', '', 'R'),
    ('q2', '1'): ('q2','1','R'),
    ('q2', '0'): ('q3','#','R'),
    ('q2', '#'): ('q3','#','R'),
    ('q3', '1'): ('q4','#','R'),
    ('q3', '0'): ('q15','#','L'),
    ('q3', '#'): ('q4','#','R'),
    ('q4', '1'): ('q4','1','R'),
    ('q4', ''): ('q5','#','R'),
    ('q4', '#'): ('q5','#','R'),
    ('q5', '1'): ('q5','1','R'),
    ('q5', ''): ('q6','1','L'),
    ('q6', '#'): ('q7','#','L'),
    ('q6', '1'): ('q6','1','L'),
    ('q7', '#'): ('q9','1','L'),
    ('q7', '1'): ('q8','1','L'),
    ('q8', '#'): ('q3','1','R'),
    ('q8', '1'): ('q8','1','L'),
    ('q9', '#'): ('q10','#','L'),
    ('q9', '1'): ('q9','1','L'),
    ('q10', '#'): ('q12','','R'),
    ('q10', '1'): ('q11','1','L'),
    ('q11', '#'): ('q0','','R'),
    ('q11', '1'): ('q11','1','L'),
    ('q12', '#'): ('q12','','R'),
    ('q12', '1'): ('q13','#','R'),
    ('q13', '#'): ('q14','','L'),
    ('q13', '1'): ('q13','#','R'),
    ('q13', ''): ('qa','','L'),
    ('q14', '#'): ('q14','','L'),
    ('q14', '1'): ('q14','#','R'),
    ('q14', ''): ('qa','','L'),
    ('q15', '#'): ('q16','','L'),
    ('q15', '1'): ('q15','#','L'),
    ('q15', ''): ('qa','','L'),
    ('q16', '#'): ('qa','','L'),
    ('q16', ''): ('qa','','L'),
    ('q16', '1'): ('q16','#','L'),
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)
        print()

    run("110111")     # 2*3 -> 111111
    run("11101111")   
    run("01111")