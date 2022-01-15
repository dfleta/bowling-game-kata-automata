
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
        self.states = {'n', '/', 'X', 'finalFrame'} # Q

        self.transitions = dict.fromkeys(self.symbols[0:10], 'n')
        # {'-': 'n', '1': 'n', '2': 'n', '3': 'n', '4': 'n', '5': 'n', '6': 'n', '7': 'n', '8': 'n', '9': 'n'}
        self.strike = {'X': 'X'}
        self.transitions.update(self.strike)
        self.spare  = {'/': '/'}
        self.transitions.update(self.spare)
        
        self.o = 'n' # initial state
        self.q = 'n' # current state
        self.p = 'n'  # next state
        self.F = 'finalFrame'
        self.state = (self.o, self.q, self.p)
        
        self.input = ""
        # Moore / Mealy
        self.lambda_output = {'-': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10, '/': 10}

        self.transition_table = { ('n', 'n', 'n'): self.lambda_frame,
                             ('n', 'n', '/'): self.lambda_spare,
                             ('n', '/', 'n'): self.lambda_roll,
                             ('/', 'n', 'n'): self.lambda_frame,
                             ('/', 'n', '/'): self.lambda_spare,
                             ('n', 'n', 'X'): self.lambda_roll,
                             ('n', 'X', 'n'): self.lambda_roll,
                             ('X', 'n', 'n'): self.lambda_double,
                             ('n', 'X', 'X'): self.lambda_double,
                             ('X', 'X', 'n'): self.lambda_strike,
                             ('X', 'X', 'X'): self.lambda_strike }

    def transition(self, symbol): # δ
        # return state p
        self.o = self.q
        self.q = self.p
        self.p = self.transitions[symbol]
        self.state = (self.o, self.q, self.p)

    def lambda_f(self, i, symbol, input):
        output = self.transition_table[self.state]
        return output(i, symbol, input)

    def lambda_roll(self, i, symbol, input):
        return self.lambda_output[symbol]

    def lambda_pass(self, i, symbol, input):
        return 0

    def lambda_frame(self, i, symbol, input):
        return self.lambda_output[symbol] + self.lambda_output[input[i - 1]]

    def lambda_spare(self, i, symbol, input):
        return self.lambda_output[symbol]

    def lambda_double(self, i, symbol, input):
        return self.lambda_output[symbol] * self.DOUBLE

    def lambda_strike(self, i, symbol, input):
        return self.lambda_output[symbol] * self.TRIPLE

    def setInput(self, input):
        self.input = list(input)

    def output(self):
        score = 0
        for i, pin in enumerate(self.input):
            self.transition(pin)
            score += self.lambda_f(i, pin, self.input)
        return score


if __name__ == "__main__":

    automata = Automaton()

    # Hitting pins total = 60
    pins = "12345123451234512345"
    total = 60
    automata.setInput(pins)
    print(automata.output())
    assert automata.output() == total

    # test symbol -
    pins = "9-9-9-9-9-9-9-9-9-9-"
    total = 90
    automata.setInput(pins)
    assert automata.output() == total

    # test spare not extra
    pins = "9-3/613/815/-/8-7/8-"
    total = 121
    automata.setInput(pins)
    assert automata.output() == total

    # test strike
    pins = "X9-9-9-9-9-9-9-9-9-"
    total = 100
    automata.setInput(pins)
    assert automata.output() == total

    pins = "X9-X9-9-9-9-9-9-9-"
    total = 110
    automata.setInput(pins)
    assert automata.output() == total
    
    # two strikes in a row is a double
    pins = "XX9-9-9-9-9-9-9-9-"
    total = 120
    automata.setInput(pins)
    assert automata.output() == total

    # three strikes in a row is a triple
    pins = "XXX9-9-9-9-9-9-9-"
    total = 141
    automata.setInput(pins)
    assert automata.output() == total

    # 12 strikes is a “Thanksgiving Turkey”.
    pins = "XXXXXXXXXXXX"
    total = 300

    pins = "9-3/613/815/-/8-7/8/8"
    total = 131

    pins = "5/5/5/5/5/5/5/5/5/5/5"
    total = 150
