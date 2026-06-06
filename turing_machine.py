# -*- coding: utf-8 -*-
"""A Turing machine simulator."""

import logging
from itertools import islice

logging.basicConfig(level=logging.WARNING, format='%(message)s')


class TuringMachine:
    """Turing machine simulator class."""

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
            tape_list = list(input_)
        else:
            tape_list = list(input_)
        
        if not tape_list:
            tape_list = [self.blank_symbol]
        
        left_side = []
        current_symbol = tape_list[0] if tape_list else self.blank_symbol
        right_side = tape_list[1:] if len(tape_list) > 1 else []
        
        state = self.start_state
        
        while True:
            config = {
                'state': state,
                'left_hand_side': left_side.copy(),
                'symbol': current_symbol,
                'right_hand_side': right_side.copy()
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
            
            current_symbol = write_symbol
            
            if direction == 'L' or direction == 'l':
                if left_side:
                    current_symbol = left_side.pop()
                else:
                    if not self.two_way_tape:
                        logging.warning("Warning: Moving left beyond leftmost cell in singly-infinite tape")
                    current_symbol = self.blank_symbol
            
            elif direction == 'R' or direction == 'r':
                if right_side:
                    current_symbol = right_side.pop(0)
                    left_side.append(write_symbol)
                else:
                    left_side.append(write_symbol)
                    current_symbol = self.blank_symbol
            
            else:
                raise ValueError(f"Unknown direction: {direction}")
            
            state = next_state
    
    def accepts(self, input_, step_limit=100):
        steps = list(islice(self.run(input_), step_limit))
        
        if not steps:
            logging.warning(f"Step limit {step_limit} reached without halting")
            return None
        
        final_action, _ = steps[-1]
        
        if final_action == 'Accept':
            return True
        elif final_action == 'Reject':
            return False
        else:
            logging.warning(f"Step limit {step_limit} reached without halting")
            return None
    
    def rejects(self, input_, step_limit=100):
        result = self.accepts(input_, step_limit)
        if result is None:
            return None
        return not result
    
    def debug(self, input_, step_limit=100, colored=False):
        print(f"\nDebugging: input = '{input_}'")
        print("-" * 50)
        
        for step_num, (action, config) in enumerate(islice(self.run(input_), step_limit)):
            state = config['state']
            left = config['left_hand_side']
            symbol = config['symbol']
            right = config['right_hand_side']
            
            tape_display = []
            
            left_part = ''.join(reversed(left))
            if left_part:
                tape_display.append(left_part)
            
            symbol_str = symbol if symbol != '' else '□'
            tape_display.append(f"[{symbol_str}]")
            
            right_part = ''.join(right)
            if right_part:
                tape_display.append(right_part)
            
            tape_str = ''.join(tape_display)
            
            print(f"Step {step_num:3d}: state={state:8s} | tape: {tape_str}")
            
            if action is not None:
                print(f"\n>>> Machine {action}ED at step {step_num} <<<\n")
                break
        else:
            print(f"\n>>> Step limit {step_limit} reached without halting <<<\n")