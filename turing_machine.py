# -*- coding: utf-8 -*-
import logging
from itertools import islice

logging.basicConfig(level=logging.WARNING, format='%(message)s')


class TuringMachine:

    def __init__(
            self,
            transitions,
            start_state='q0',
            accept_state='qa',
            reject_state='qr',
            blank_symbol=''
    ):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.two_way_tape = False

    def enable_two_way_tape(self):
        self.two_way_tape = True

    def run(self, input_):
        tape = list(input_)
        if len(tape) == 0:
            tape = [self.blank_symbol]

        state = self.start_state
        head_pos = 0

        while True:
            if head_pos < 0:
                if self.two_way_tape:
                    tape.insert(0, self.blank_symbol)
                    head_pos = 0
                else:
                    head_pos = 0
            
            if head_pos >= len(tape):
                current_symbol = self.blank_symbol
            else:
                current_symbol = tape[head_pos]

            left_part = tape[:head_pos]
            right_part = tape[head_pos + 1:] if head_pos + 1 < len(tape) else []
            
            config = {
                'state': state,
                'left_hand_side': list(reversed(left_part)),
                'symbol': current_symbol,
                'right_hand_side': right_part
            }

            if state == self.accept_state:
                yield ('Accept', config)
                return

            if state == self.reject_state:
                yield ('Reject', config)
                return

            yield (None, config)

            key = (state, current_symbol)
            
            if key not in self.transitions:
                state = self.reject_state
                continue

            next_state, write_symbol, direction = self.transitions[key]

            while head_pos >= len(tape):
                tape.append(self.blank_symbol)
            
            tape[head_pos] = write_symbol

            if direction.upper() == 'R':
                head_pos += 1
            elif direction.upper() == 'L':
                head_pos -= 1
            else:
                raise ValueError(f'Invalid direction: {direction}')

            state = next_state

    def accepts(self, input_, step_limit=100):
        steps = 0
        for action, _ in self.run(input_):
            steps += 1
            if steps > step_limit:
                logging.warning(f'Step limit {step_limit} reached without halting')
                return None
            if action == 'Accept':
                return True
            if action == 'Reject':
                return False
        return None

    def rejects(self, input_, step_limit=100):
        result = self.accepts(input_, step_limit=step_limit)
        if result is None:
            return None
        return not result

    def debug(self, input_, step_limit=100, colored=False):
        print(f'\nDebugging: input = "{input_}"')
        print('-' * 50)

        for i, (action, config) in enumerate(islice(self.run(input_), step_limit)):
            state = config['state']
            left_str = ''.join(reversed(config['left_hand_side']))
            symbol = config['symbol'] if config['symbol'] != '' else '_'
            right_str = ''.join(config['right_hand_side'])
            print(f'Step {i:3d}: state={state:8s} | tape: {left_str}[{symbol}]{right_str}')

            if action is not None:
                print(f'\n>>> Machine {action}ED at step {i} <<<\n')
                return

        print(f'\n>>> Step limit {step_limit} reached without halting <<<\n')