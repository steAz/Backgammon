from AImove import AImove
from BoardState import BoardState
from GameField import *
import copy

class AIboardState(BoardState):
    
    def __init__(self, move, numOfMoves = 0, startingBoardState = None):
        if startingBoardState == None:
            self._botMove = move
            self._heuristic = 0
            self._diceI = 0
            self._diceII = 0
            self._numberOfMoves = numOfMoves
            self._botMove._amountOfMoves = self._numberOfMoves
            self._fields_states = []
            self._redsOnBand = 0
            self._blacksOnBand = 0
            self._blacksOnTheCourt = 0
            self._redsOnTheCourt = 0
        else:
            self._botMove = move
            self._heuristic = 0
            self._diceI = 0
            self._diceII = 0
            self._numberOfMoves = numOfMoves
            self._botMove._amountOfMoves = self._numberOfMoves
            self._redsOnBand = startingBoardState._redsOnBand
            self._blacksOnBand = startingBoardState._blacksOnBand
            self._blacksOnTheCourt = startingBoardState._blacksOnTheCourt
            self._redsOnTheCourt = startingBoardState._redsOnTheCourt

            self._fields_states = []
            for field in startingBoardState._fields_states:
                self._fields_states.append(copy.deepcopy(field))

            

    def AIbStateAfterMove(self):
        #move.makeAImove(self)
        self. _heuristic = self.calculateHeuristic()
        self._numberOfMoves -= 1
        self._botMove._amountOfMoves -= 1


    def calculateHeuristic(self):
        resultBlack = 0
        resultRed = 0
        index = 0
        #calculating black

        resultBlack += 15 * self._redsOnBand
        resultRed += 15 * self._blacksOnBand

        for field in self._fields_states:
            if field._is_empty == False and field._color == Color.BLACK:
                if index < 18:
                    resultBlack += index
                    if field._number_of_checkers > 1:
                        resultBlack += 3 * index
                else:
                    resultBlack += (index - 15)
                    if field._number_of_checkers > 1:
                        resultBlack += 3 * (index - 15)
            index += 1
        index = 0
        for field in self._fields_states:
            if field._is_empty == False and field._color == Color.RED:
                if index > 5:
                    resultRed += (23 - index)
                    if field._number_of_checkers > 1:
                        resultBlack += 3 * (23 - index)
                else:
                    resultRed += (8 - index)
                    if field._number_of_checkers > 1:
                        resultBlack += 3 * (8 - index)
            index += 1

        return (resultBlack - resultRed)



