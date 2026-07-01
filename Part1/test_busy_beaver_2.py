# -*- coding: utf-8 -*-
from turing_machine import TuringMachine

# Python generators are useful for Turing machines because they invert control
# over to the caller. They can generate an output stream lazily
# ...

#create the Turing machine
bbeaver2 = TuringMachine(
    { 
        # 2-state Busy Beaver
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)
bbeaver3 = TuringMachine(
    {
        # 3-state Busy Beaver
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('h', '1', 'R'),
        ('b', '0'): ('c', '0', 'R'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('c', '1', 'L'),
        ('c', '1'): ('a', '1', 'L'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)
bbeaver4 = TuringMachine(
    {
        # 4-state Busy Beaver
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('c', '0', 'L'),
        ('c', '0'): ('h', '1', 'R'),
        ('c', '1'): ('d', '1', 'L'),
        ('d', '0'): ('d', '1', 'R'),
        ('d', '1'): ('a', '0', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)


if __name__ == "__main__":
    def run(input_):
        w = input_
        print("BB with 2 states")
        bbeaver2.debug(w, step_limit=1000)
        print()
        print("BB with 3 states")
        bbeaver3.debug(w, step_limit=1000)
        print()
        print("BB with 4 states")
        bbeaver4.debug(w, step_limit=1000)
        print()

    run('00000000000000')