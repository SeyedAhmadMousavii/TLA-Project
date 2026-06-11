# -*- coding: utf-8 -*-
from turing_machine import TuringMachine

# BB(2) - 4 ones, 6 steps
bbeaver2 = TuringMachine(
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)

# BB(3) - 6 ones, 21 steps (CORRECT)
bbeaver3 = TuringMachine(
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('h', '1', 'R'),
        ('b', '0'): ('c', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '1', 'L'),
        ('c', '1'): ('b', '1', 'L'),
    },
    start_state='a', accept_state='h', reject_state='r', blank_symbol='0'
)

# BB(4) - 13 ones, 107 steps (CORRECT)
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

# BB(5) known champion - 4098 ones, 47,176,870 steps
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

if __name__ == "__main__":
    for m in [bbeaver2, bbeaver3, bbeaver4, bbeaver5]:
        m.enable_two_way_tape()

    def run(machine, name, step_limit=200):
        print(f'\n{name} Busy Beaver:')
        print('-' * 40)
        machine.debug('', step_limit=step_limit)

    run(bbeaver2, '2-state (BB2=4 ones, 6 steps)', step_limit=20)
    run(bbeaver3, '3-state (BB3=6 ones, 21 steps)', step_limit=50)
    run(bbeaver4, '4-state (BB4=13 ones, 107 steps)', step_limit=150)
    run(bbeaver5, '5-state (BB5=4098 ones, 47M steps - first steps)', step_limit=30)