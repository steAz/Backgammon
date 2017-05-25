from logic.AImove import AImove
from model.BoardState import BoardState
import copy

class AIboardState(BoardState):
    
    def __init__(self, move = None, numOfMoves=None, startingBoardState = None):
        if startingBoardState == None:
            self.__botMove = move
            self.__heuristic = 0
            self.__diceI = 0
            self.__diceII = 0
            self.__numberOfMoves = numOfMoves
            self.__fields_states = []
            self.__redsOnBand = 0
            self.__blacksOnBand = 0
            self.__blacksOnTheCourt = 0
            self.__redsOnTheCourt = 0
        else:
            self.__botMove = move
            self.__heuristic = 0
            self.__diceI = 0
            self.__diceII = 0
            self.__numberOfMoves = numOfMoves
            self.__redsOnBand = startingBoardState._BoardState__redsOnBand
            self.__blacksOnBand = startingBoardState._BoardState__blacksOnBand
            self.__blacksOnTheCourt = startingBoardState._BoardState__blacksOnTheCourt
            self.__redsOnTheCourt = startingBoardState._BoardState__redsOnTheCourt

            self.__fields_states = []
            for field in startingBoardState._BoardState__fields_states:
                self.__fields_states.append(copy.deepcopy(field))

            

    def AIbStateAfterMove(self):
        #move.makeAImove(self)
        self. __heuristic = self.calculateHeuristic()
        self.__numberOfMoves -= 1


    def calculateHeuristic(self):
        resultBlack = 0
        index = 0
        #calculating black
        for field in self.__fields_states:
            if field.is_empty == False and field.color == Color.BLACK:
                if index < 18:
                    resultBlack += index
                else:
                    resultBlack += (index - 15)
            index += 1
        index = 0
        for field in self.__fields_states:
            if field.is_empty == False and field.color == Color.RED:
                if index > 5:
                    resultRed += (23 - index)
                else:
                    resultRed += (8 - index)
            index += 1

        return (resultBlack - resultRed)



