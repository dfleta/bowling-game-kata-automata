import pytest

from src.automaton import Automaton
from src.automaton import ScoreCard

@pytest.mark.state_n
def test_hitting_pins_regular():
    # Hitting pins total = 60
    automata = Automaton()
    pins = "12345123451234512345"
    total = 60
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.state_n
def test_symbol_zero():
    # test symbol -
    automata = Automaton()
    pins = "9-9-9-9-9-9-9-9-9-9-"
    total = 90
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

    automata = Automaton()
    pins = "9-3561368153258-7181"
    total = 82
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.spare
def test_spare_not_extra():
    # test spare not extra
    automata = Automaton()
    pins = "9-3/613/815/-/8-7/8-"
    total = 121
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.strike
def test_strike():
    # test strike
    automata = Automaton()
    pins = "X9-9-9-9-9-9-9-9-9-"
    total = 100
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

    automata = Automaton()
    pins = "X9-X9-9-9-9-9-9-9-"
    total = 110
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.strike
def test_two_strikes(): 
    # two strikes in a row is a double
    automata = Automaton()
    pins = "XX9-9-9-9-9-9-9-9-"
    total = 120
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.strike
def test_three_strikes():
    # three strikes in a row is a triple
    automata = Automaton()
    pins = "XXX9-9-9-9-9-9-9-"
    total = 141
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.extra_rolls
def test_one_pin_in_extra_roll():
    # one pin in extra roll
    automata = Automaton()
    pins = "9-3/613/815/-/8-7/8/8"
    total = 131
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

    automata = Automaton()
    pins = "5/5/5/5/5/5/5/5/5/5/5"
    total = 150
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.extra_rolls
def test_two_strikes_in_extra_rolls():
    # two strikes in extra rolls
    automata = Automaton()
    pins = "9-9-9-9-9-9-9-9-9-XXX"
    total = 111
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.extra_rolls
def test_one_strike_in_extra_roll():
    # one strike in extra roll
    automata = Automaton()
    pins = "8/549-XX5/53639/9/X"
    total = 149
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.extra_rolls
def test_spare_in_extra_roll():
    # spare in extra roll
    automata = Automaton()
    pins = "X5/X5/XX5/--5/X5/"
    total = 175
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total

@pytest.mark.extra_rolls
def test_triple_strike_before_extra_rolls():
    # 12 strikes is a “Thanksgiving Turkey”
    # 2 strikes in extra rolls
    automata = Automaton()
    pins = "XXXXXXXXXXXX"
    total = 300
    scoreCard = ScoreCard(pins)
    automata.setInput(scoreCard)
    assert automata.output() == total
