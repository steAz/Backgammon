
from enum import Enum
from logic.AImove import AImove
import copy

class TraversingLevel(Enum):
    MAX = 0
    MIN = 1
    CHANCE = 2

class AIBot(object):
    
    def __init__(self):
        pass

    def generateBoardStates(self, startingBoard):
        newNumberOfMoves = startingBoard.__numberOfMoves - 1
        if newNumberOfMoves > 0:
            pass
        else:

            #generating new boards with new dice roll (CHANCE level)
            for i in range(1, 7):
                for j in range(i, 7):
                    pass


    def boardStatesFromDice(self, currBoard, diceNum, currColor):
        #generates all boardStates available: from currBoard using diceNumber roll( diceNumber == <1;6> )
        AIboards = []
        fieldIndex = 0
        for field in currBoard.fields_states:
            if currColor == field.__color and field.__is_empty == False:
                newBoard = copy.deepcopy(currBoard)
                newBoard.__AImove = AImove(diceNum, fieldIndex, currColor)
                isValidMove = newBoard.__AImove.makeTurn(newBoard, index, currColor)
                if isValidMove == True:
                    AIboards.append(newBoard)
            fieldIndex += 1

        return AIboards




