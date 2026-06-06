# -*- coding: utf-8 -*-
import logging
from itertools import islice

logging.basicConfig(level=logging.WARNING, format='%(message)s')


class TuringMachine:
    
    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.two_way_tape = False
    
    def enable_two_way_tape(self):
        self.two_way_tape = True
    
    def run(self, input_):
        if isinstance(input_, str):
            tape = list(input_)
        else:
            tape = list(input_)
        
        if not tape:
            tape = [self.blank_symbol]
        
        state = self.start_state
        head_pos = 0
        
        while True:
            left = tape[:head_pos]
            current_symbol = tape[head_pos] if head_pos < len(tape) else self.blank_symbol
            right = tape[head_pos + 1:] if head_pos + 1 < len(tape) else []
            
            config = {
                'state': state,
                'left_hand_side': list(reversed(left)),
                'symbol': current_symbol,
                'right_hand_side': right
            }
            
            if state == self.accept_state:
                yield ('Accept', config)
                return
            elif state == self.reject_state:
                yield ('Reject', config)
                return
            
            yield (None, config)
            
            key = (state, current_symbol)
            
            if key not in self.transitions:
                state = self.reject_state
                continue
            
            next_state, write_symbol, direction = self.transitions[key]
            
            tape[head_pos] = write_symbol
            
            if direction == 'L' or direction == 'l':
                head_pos -= 1
                if head_pos < 0:
                    if not self.two_way_tape:
                        logging.warning('Moving left beyond leftmost cell in singly-infinite tape')
                    tape.insert(0, self.blank_symbol)
                    head_pos = 0
            elif direction == 'R' or direction == 'r':
                head_pos += 1
                if head_pos >= len(tape):
                    tape.append(self.blank_symbol)
            else:
                raise ValueError(f'Invalid direction: {direction}')
            
            state = next_state
    
    def accepts(self, input_, step_limit=100):
        steps = list(islice(self.run(input_), step_limit))
        
        if not steps:
            logging.warning(f'Step limit {step_limit} reached without halting')
            return None
        
        action, _ = steps[-1]
        
        if action == 'Accept':
            return True
        elif action == 'Reject':
            return False
        else:
            logging.warning(f'Step limit {step_limit} reached without halting')
            return None
    
    def rejects(self, input_, step_limit=100):
        result = self.accepts(input_, step_limit)
        if result is None:
            return None
        return not result
    
    def debug(self, input_, step_limit=100, colored=False):
        print(f'\nDebugging: input = "{input_}"')
        print('-' * 50)
        
        for i, (action, config) in enumerate(islice(self.run(input_), step_limit)):
            state = config['state']
            left = ''.join(reversed(config['left_hand_side']))
            symbol = config['symbol'] if config['symbol'] != '' else '□'
            right = ''.join(config['right_hand_side'])
            
            print(f'Step {i:3d}: state={state:8s} | tape: {left}[{symbol}]{right}')
            
            if action is not None:
                print(f'\n>>> Machine {action}ED at step {i} <<<\n')
                return
        
        print(f'\n>>> Step limit {step_limit} reached without halting <<<\n')