from model.GameField import Color
from logic.Game import Game

class Move(object):
   
    def __init__(self, game):
        self.__fieldNumber = 0
        self.__rollNumber = 0
        self.__color
        self.__game = game

    def boardStateAfterMove(self, currentBoardState):
        if self.__color == __color.RED:
            destField = self.__fieldNumber - self.__rollNumber
            pass


