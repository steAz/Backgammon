from Game import Game
from GameField import Color

class AImove(Game):
    def __init__(self, color, diceNum, diceNumI, diceNumII, fieldNum, amountOfMoves, bandMove=False):
        self._currNum = diceNum
        self._fieldNum = fieldNum
        self._color = color
        self._amountOfMoves = amountOfMoves
        self._currNumI = diceNumI
        self._currNumII = diceNumII
        self._isBandMove = bandMove#if true it's move from band
        
    def makeAImove(self, AIboard):
        #if self._isBandMove == False:
            #self.makeTurn(AIboard, self._fieldNum, self._color)
        #else:
            #self.removeFromBand(self._color, AIboard)
        if (self._color == Color.BLACK and AIboard._blacksOnBand > 0) or (self._color == Color.RED and AIboard._redsOnBand > 0):
            self.removeFromBand(self._color, AIboard)
            if self._color == Color.RED:
                self._destField = AIboard._fields_states[24 - self._currNum]
            else:
                self._destField = AIboard._fields_states[self._currNum - 1]
        else:
            self.makeTurn(AIboard, self._fieldNum, self._color)
         


