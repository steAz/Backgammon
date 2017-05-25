from logic.Game import Game

class AImove(Game):
    def __init__(self, color, diceNum = None, fieldNum = None):
        self.__currNum = diceNum
        self.__fieldNum = fieldNum
        self.__color = color
        
    def makeAImove(self, AIboard):
        self.makeTurn(AIboard, self.__fieldNum, self.__color)
         


