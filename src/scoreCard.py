
class ScoreCard:

    def __init__(self, scoreCard):
        self.pins = scoreCard
        self.LAST_FRAME = 10
        self.frame = 1
        self.score = 0

    def frame_pins(self, roll):
        frame_pins = self.pins[roll]
        if frame_pins not in ['/', 'X']:
            frame_pins += self.pins[roll + 1]
            roll += 1
        return roll, frame_pins

