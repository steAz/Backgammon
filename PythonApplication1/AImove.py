from Game import Game

class AImove(Game):
    def __init__(self, color, diceNum, fieldNum, amountOfMoves):
        self._currNum = diceNum
        self._fieldNum = fieldNum
        self._color = color
        self._amountOfMoves = amountOfMoves
        
    def makeAImove(self, AIboard):
        self.makeTurn(AIboard, self._fieldNum, self._color)
         


