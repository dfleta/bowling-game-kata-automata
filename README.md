# Bowling Game Kata

[Uncle Bob teach a the desing process through TDD](http://www.butunclebob.com/ArticleS.UncleBob.TheBowlingGameKata)

Extract from [Emily Bache](https://github.com/emilybache) "The Coding Dojo Handbook":

-------------
Create a program, which, given a valid sequence of rolls for one line of American Ten-Pin Bowling, produces the total score for the game. This is a summary of the rules of the game:

- Each game, or “line” of bowling, includes ten turns, or “frames” for the bowler.
- In each frame, the bowler gets up to two tries to knock down all the pins.
- If in two tries, he fails to knock them all down, his score for that frame is the total number of pins knocked down in his two tries.
- If in two tries he knocks them all down, this is called a “spare” and his score for the frame is ten plus the number of pins knocked down on his next throw (in his next turn).
- If on his first try in the frame he knocks down all the pins, this is called a “strike”. His turn is over, and his score for the frame is ten plus the simple total of the pins knocked down in his next two rolls.
- If he gets a spare or strike in the last (tenth) frame, the bowler gets to throw one or two more bonus balls, respectively. These bonus throws are taken as part of the same turn. If the bonus throws knock down all the pins, the process does not repeat: the bonus throws are only used to calculate the score of the final frame.
- The game score is the total of all frame scores.

### Here are some things that the program will not do:
- We will not check for valid rolls.
- We will not check for correct number of rolls and frames.
- We will not provide scores for intermediate frames.

The input is a scorecard from a finished bowling game, where “X” stands for a strike, “-” for no pins bowled, and “/” means a spare. Otherwise figures 1-9 indicate how many pins were knocked down in that throw.

### Sample games

    12345123451234512345
always hitting pins without getting spares or strikes, a total
score of 60

    XXXXXXXXXXXX
a perfect game, 12 strikes, giving a score of 300

    9-9-9-9-9-9-9-9-9-9-
heartbreak - 9 pins down each round, giving a score of 90

    5/5/5/5/5/5/5/5/5/5/5
a spare every round, giving a score of 150

-------------------

## Solution

I have tried to solve the problem using finite states automata theory. 

My approach is not 100% formal but focusing in DDD (domain driven desing), that is, automaton facilitates the expression of the logic (and the algorithm) of the problem in a well defined notation, also for the bowling game vocabulary as well.

A finite automaton is a collection of 5-tuple (Q, ∑, δ, q0, F), where:

    Q: finite set of states  
    ∑: finite set of the input symbol  
    q0: initial state   
    F: final state  
    δ: Transition function
    λ: output function

I have included the lambda (`λ`) output function proposed in the Mealy Machine to compute the output of each transition between two states. The output is the decimal value of the points achieved in that specific frame, besides the future update in the game score if the state is spare or strike.

Each frame means a change in the state of the machine. The automaton computes the pins in a frame to define the `a` symbol and call the transition function `δ(q, a) = p`, where `q` is the actual state and `p` the next state.

The automaton reads the score card as a string of input symbols and moves between states `n` (regular roll), `/` spare, `X` strike or `extra_rolls`.

### TDD

The proposed order of the test cases is crucial to develop an "organic" algorithm.

Is mandatory to run `coverage` in both test and `Automaton` and `ScoreCard` classes.

    > coverage run -m pytest
    > coverage report -m

Pytest `markers` facilitate the selection and focusing in the transition to the required state.

VSCode test debugging in addition with breakpoints are valuable tools to understand the code.
