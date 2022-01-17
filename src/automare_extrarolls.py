import re
from src.scoreCard import ScoreCard

''' 
A finite automaton is a collection of 5-tuple (Q, ∑, δ, q0, F), where:

    Q: finite set of states  
    ∑: finite set of the input symbol  
    q0: initial state   
    F: final state  
    δ: Transition function. δ(q, a) = p
    λ: output function
'''

class Automaton:

    def __init__(self):

        ### 
        # Automata definition 
        # ###

        self.symbols = "-123456789/X"
        self.alphabet = set(self.symbols) # ∑
        self.states = {'n', '/', 'X', 'extra_rolls'} # Q
        self.o = 'n' # initial state
        self.q = 'n' # current state
        self.p = 'n'  # next state
        self.F = 'extra_rolls' # final state
        self.state = (self.o, self.q, self.p)

        ###
        # δ: Transition function
        # ###
    
        self.transitions = {'n': 'n'}
        self.strike = {'X': 'X'}
        self.transitions.update(self.strike)
        self.spare  = {'/': '/'}
        self.transitions.update(self.spare)

        self.pattern_pins = re.compile('[1-9][1-9]|-[1-9]|[1-9]-|--')
        self.pattern_spare = re.compile('[1-9]/|-/')
        
        ###
        # Transition table 
        # ###
        self.transition_table = { ('n', 'n', 'n'): self.lambda_two_pins,
                             ('n', 'n', '/'): self.lambda_pin_spare,
                             ('n', '/', 'n'): self.lambda_spare,
                             ('/', 'n', 'n'): self.lambda_two_pins,
                             ('/', 'n', '/'): self.lambda_pin_spare,
                             ('n', '/', '/'): self.lambda_spare_spare,
                             ('/', '/', 'n'): self.lambda_spare,
                             ('/', '/', '/'): self.lambda_spare_spare,
                             ('/', '/', 'X'): self.lambda_strike,
                             ('n', 'n', 'X'): self.lambda_two_pins,
                             ('n', 'X', 'n'): self.lambda_strike,
                             ('X', 'n', 'n'): self.lambda_two_pins,
                             ('n', 'X', 'X'): self.lambda_strike,
                             ('X', 'X', 'n'): self.lambda_double_strike,
                             ('X', 'X', 'X'): self.lambda_triple_strike,
                             ('X', 'X', '/'): self.lambda_double_strike_spare,
                             ('X', '/', 'X'): self.lambda_strike,
                             ('/', 'X', 'X'): self.lambda_strike,
                             ('/', 'X', '/'): self.lambda_strike_spare,
                             ('/', 'n', 'X'): self.lambda_two_pins,
                             ('X', '/', 'n'): self.lambda_spare,
                             ('n', 'X', '/'): self.lambda_strike_spare,
                             ('n', '/', 'X'): self.lambda_strike,
                             ('X', 'n', 'X'): self.lambda_two_pins }
        
        # INPUT
        self.input = "" # Score Card

        ### 
        # OUTPUT 
        # Mealy lambda output function 
        # ###
        self.pin_value = {'-': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10, '/': 10 }
        self.DOUBLE = 2
        self.TRIPLE = 3

    ###
    # δ: Transition function
    # ###

    def transition(self, symbol): # δ
        # return state p
        self.o = self.q
        self.q = self.p
        if self.pattern_pins.match(symbol):
            self.p = self.transitions['n']
        elif self.pattern_spare.match(symbol):
            self.p = self.transitions['/']
        elif symbol == 'X':
            self.p = self.transitions['X']
        else:
            self.p = 'extra_rolls'
        self.set_state(self.o, self.q, self.p)

    def set_state(self, o, q, p):
        self.state = (self.o, self.q, self.p)

    ###
    # Mealy lambda output function 
    # ###

    def lambda_function(self, symbol):
        output = self.transition_table[self.state]
        return output(symbol)

    def lambda_two_pins(self, symbol):
        if symbol[-1] == '/':
            return self.lambda_pin_spare(symbol)
        def int_value(symbol):
            return self.pin_value[symbol]
        return sum(map(int_value, list(symbol)))

    def lambda_pin_spare(self, symbol):
        return self.pin_value['/']

    def lambda_spare(self, symbol):
        return self.lambda_two_pins(symbol[0]) * self.DOUBLE + self.lambda_two_pins(symbol[1])
    
    def lambda_spare_spare(self, symbol):
        return self.lambda_two_pins(symbol[0]) + self.lambda_two_pins(symbol[1])

    def lambda_strike(self, symbol):
        return self.lambda_two_pins(symbol) * self.DOUBLE

    def lambda_double_strike(self, symbol):
        return self.lambda_two_pins(symbol) * self.DOUBLE + self.lambda_two_pins(symbol[0])

    def lambda_triple_strike(self, symbol):
        return self.lambda_two_pins(symbol) * self.TRIPLE

    def lambda_strike_spare(self, symbol):
        return self.lambda_pin_spare(symbol) * self.DOUBLE

    def lambda_double_strike_spare(self, symbol):
        return self.lambda_pin_spare(symbol) * self.DOUBLE + self.lambda_two_pins(symbol[0])
    

    ### 
    # INPUT 
    # ###

    def setInput(self, scoreCard):
        self.input = scoreCard

    ### 
    # OUTPUT
    # ###

    def output(self):
        roll = 0 # automaton input reader
        while self.p != self.F:
            roll, frame_pins = self.input.frame_pins(roll) # refactor 2 niveles mfowler
            self.input.frame += 1
            self.transition(frame_pins)
            self.input.score += self.lambda_function(frame_pins)
            roll += 1
            if self.input.frame > self.input.LAST_FRAME:
                self.transition('extra_rolls')

        # extra rolls
        extra_rolls = self.input.pins[roll:]
        if not extra_rolls:  # se puede mover al while de arriba
            return self.input.score
                
        if self.state == ('X', 'X', 'extra_rolls'):
            self.input.score += self.lambda_triple_strike('X')
            return self.input.score
        else:
            # casos: 5/ XX X 8
            self.input.score += self.lambda_two_pins(extra_rolls)
            return self.input.score
