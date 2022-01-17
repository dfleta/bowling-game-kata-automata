import re
from src.scoreCard import ScoreCard

''' 
A finite automaton is a collection of 5-tuple (Q, ∑, δ, q0, F), where:

    Q: finite set of states  
    ∑: finite set of the input symbol  
    q0: initial state   
    F: final state  
    δ: Transition function
    λ: output function
'''

class Automaton:

    def __init__(self):

        self.DOUBLE = 2
        self.TRIPLE = 3

        self.symbols = "-123456789/X"
        self.alphabet = set(self.symbols) # ∑
        self.states = {'n', '/', 'X', 'extra_rolls'} # Q

        # self.transitions = dict.fromkeys(self.symbols[0:10], 'n')
        # {'-': 'n', '1': 'n', '2': 'n', '3': 'n', '4': 'n', '5': 'n', '6': 'n', '7': 'n', '8': 'n', '9': 'n'}
        self.pattern_pins = re.compile('[1-9][1-9]|-[1-9]|[1-9]-|--')
        self.pattern_spare = re.compile('[1-9]/|-/')
        # self.transitions = {self.pattern: 'n'}

        self.transitions = {'n': 'n'}
        self.strike = {'X': 'X'}
        self.transitions.update(self.strike)
        self.spare  = {'/': '/'}
        self.transitions.update(self.spare)
        
        self.o = 'n' # initial state
        self.q = 'n' # current state
        self.p = 'n'  # next state
        self.F = 'extra_rolls'
        self.state = (self.o, self.q, self.p)
        
        self.input = ""
        # Moore / Mealy
        self.lambda_output = {'-': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10, '/': 10 }

        self.transition_table = { ('n', 'n', 'n'): self.lambda_pins,
                             ('n', 'n', '/'): self.lambda_pin_spare,
                             ('n', '/', 'n'): self.lambda_spare,
                             ('/', 'n', 'n'): self.lambda_pins,
                             ('/', 'n', '/'): self.lambda_pin_spare,
                             ('n', '/', '/'): self.lambda_spare_spare,
                             ('/', '/', 'n'): self.lambda_spare,
                             ('/', '/', '/'): self.lambda_spare_spare,
                             ('/', '/', 'X'): self.lambda_strike,
                             ('n', 'n', 'X'): self.lambda_pins,
                             ('n', 'X', 'n'): self.lambda_strike,
                             ('X', 'n', 'n'): self.lambda_pins,
                             ('n', 'X', 'X'): self.lambda_strike,
                             ('X', 'X', 'n'): self.lambda_double,
                             ('X', 'X', 'X'): self.lambda_triple,
                             ('X', 'X', '/'): self.lambda_double_spare,
                             ('X', '/', 'X'): self.lambda_strike,
                             ('/', 'X', 'X'): self.lambda_strike,
                             ('/', 'X', '/'): self.lambda_strike_spare,
                             ('/', 'n', 'X'): self.lambda_pins,
                             ('X', '/', 'n'): self.lambda_spare,
                             ('n', 'X', '/'): self.lambda_strike_spare,
                             ('n', '/', 'X'): self.lambda_strike,
                             ('X', 'n', 'X'): self.lambda_pins }

    def transition(self, symbol): # δ
        # return state p
        self.o = self.q
        self.q = self.p
        if self.pattern_pins.match(symbol):
            self.p = self.transitions['n']
        elif self.pattern_spare.match(symbol):
            self.p = self.transitions['/']
        else:
            self.p = self.transitions['X']
        self.set_state()

    def set_state(self):
        self.state = (self.o, self.q, self.p)

    def lambda_function(self, symbol):
        output = self.transition_table[self.state]
        return output(symbol)

    def lambda_pins(self, symbol):
        if symbol[-1] == '/':
            return self.lambda_pin_spare(symbol)
        def int_value(symbol):
            return self.lambda_output[symbol]
        return sum(map(int_value, list(symbol)))

    def lambda_pin_spare(self, symbol):
        return self.lambda_output['/']

    def lambda_spare(self, symbol):
        return self.lambda_pins(symbol[0]) * self.DOUBLE + self.lambda_pins(symbol[1])
    
    def lambda_spare_spare(self, symbol):
        return self.lambda_pins(symbol[0]) + self.lambda_pins(symbol[1])

    def lambda_strike(self, symbol):
        return self.lambda_pins(symbol) * self.DOUBLE

    def lambda_triple(self, symbol):
        return self.lambda_pins(symbol) * self.TRIPLE

    def lambda_double(self, symbol):
        return self.lambda_pins(symbol) * self.DOUBLE + self.lambda_pins(symbol[0])

    def lambda_double_spare(self, symbol):
        return self.lambda_pin_spare(symbol) * self.DOUBLE + self.lambda_pins(symbol[0])
    
    def lambda_strike_spare(self, symbol):
        return self.lambda_pin_spare(symbol) * self.DOUBLE

    def setInput(self, scoreCard):
        self.input = scoreCard

    def output(self):
        frame_d = 0 # debugging
        score_d = 0 # debugging
        roll = 0 # automaton input reader
        # while i < len(self.input.pins): # refactorizar a no estar en last frame, i sobra aqui
        while self.p != 'extra_rolls':
            roll, frame_pins = self.input.frame_pins(roll) # refactor 2 niveles mfowler
            self.transition(frame_pins)
            self.input.score += self.lambda_function(frame_pins)
            score_d = self.input.score # debugging
            roll += 1
            self.input.frame += 1
            frame_d = self.input.frame #debugging
            if self.input.frame > 10:
                self.p = 'extra_rolls'
                self.set_state()

        # extra rolls
        extraRolls = self.input.pins[roll:]
        if not extraRolls:  # se puede mover al while de arriba
            return self.input.score
                
        if self.state == ('X', 'X', 'extra_rolls'):
            self.input.score += self.lambda_triple('X')
            return self.input.score

        # casos: 5/ XX X 8
        self.input.score += self.lambda_pins(extraRolls)
        score_d = self.input.score # debug
        return self.input.score
