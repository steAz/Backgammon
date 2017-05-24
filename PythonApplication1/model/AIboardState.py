from logic.AImove import AImove
from model.BoardState import BoardState

class AIboardState(BoardState):
    
    def __init__(self, move, numOfMoves):
        self.__AImove = move
        self.__heuristic = 0
        self.__diceI = 0
        self.__diceII = 0
        self.__numberOfMoves = numOfMoves


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



