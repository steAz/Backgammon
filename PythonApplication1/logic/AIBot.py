
from enum import Enum
from logic.AImove import AImove
from model.AIboardState import AIboardState
from random import randint
import copy
import sys

class TraversingLevel(Enum):
    MAX = 0
    MIN = 1
    CHANCE = 2
from logic.AImove import AImove

class AIbot(object):
    
    def __init__(self):
        self.__moveI = 0
        self.__moveII = 0


    def generateChildrenBoardStates(self, startingBoard):
        newNumberOfMoves = startingBoard._AIboardState__numberOfMoves
        if newNumberOfMoves > 0:
            if newNumberOfMoves == 1:
                return self.boardStatesFromDice(startingBoard, startingBoard.__diceI, startingBoard.__AImove.__color)
            else:
                return self.boardStatesFromDice(startingBoard, startingBoard.__diceII, startingBoard.__AImove.__color)
        else:
            AIboards = []
            #generating new boards with new dice roll (CHANCE level)
            for i in range(1, 7):
                for j in range(i, 7):
                    newBoard = copy.deepcopy(startingBoard)
                    newBoard.__diceI = i
                    newBoard.__diceII = j
                    if i != j: 
                        newBoard.__numberOfMoves = 2
                    else:
                         newBoard.__numberOfMoves = 4
                    AIboards.append(newBoard)
            return Aiboards


    def boardStatesFromDice(self, currBoard, diceNum, currColor):
        #generates all boardStates available: from currBoard using diceNumber roll( diceNumber == <1;6> )
        AIboards = []
        fieldIndex = 0
        for field in currBoard.fields_states:
            if currColor == field.__color and field.__is_empty == False:
                newBoard = copy.deepcopy(currBoard)
                newBoard.__AImove = AImove(diceNum, fieldIndex, currColor)
                isValidMove = newBoard.__AImove.makeTurn(newBoard, fieldIndex, currColor)
                if isValidMove == True:
                    newBoard.AIbStateAfterMove() #calculated move and heuristic for one board in state
                    AIboards.append(newBoard)
            fieldIndex += 1

        return AIboards


    def maxMinChanceEvaluateState(self, currBoard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel):
        if currDepth == maxDepth:
            return currBoard.__heuristic
        
        AIchildrenBoards = self.generateChildrenBoardStates(currBoard)
        nextTypeOfLevel = self.setNextTraversingLevel(currBoard, typeOfLevel, previousTypeOfLevel)
        if typeOfLevel == TraversingLevel.MIN:
            heuristic_V = sys.minint
            for AIchildBoard in AIchildrenBoards:
                newBoard = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if newBoard.__heuristic < heuristic_V:
                    heuristic_V = newBoard.__heuristic
        elif typeOfLevel == TraversingLevel.MAX:
            heuristic_V = sys.maxint
            for AIchildBoard in AIchildrenBoards:
                newBoard = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if newBoard.__heuristic > heuristic_V:
                    heuristic_V = newBoard.__heuristic
                    if currDepth == 2:
                        self.__moveII = newBoard.__AImove
                    elif currDepth == 1:
                        self.__moveI = newBoard.__AImove
        elif typeOfLevel == TraversingLevel.CHANCE:
            heuristic_V = 0 
            for AIchildBoard in AIchildrenBoards:
                newBoard = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                probabilityOfAIchildBoard = 1/21
                heuristic_V += probabilityOfAIchildBoard * newBoard.__heuristic

        return heuristic_V


    def setNextTraversingLevel(self, currBoard, typeOfLevel, previousTypeOfLevel):
        if typeOfLevel == TraversingLevel.MIN:
            if currBoard.__numberOfMoves == 1:
                    nextTypeOfLevel = TraversingLevel.CHANCE
            else:
                    nextTypeOfLevel = TraversingLevel.MIN
        elif typeOfLevel == TraversingLevel.MAX:
            if currBoard.__numberOfMoves == 1:
                nextTypeOfLevel = TraversingLevel.CHANCE
            else:
                nextTypeOfLevel = TraversingLevel.MAX
        elif typeOfLevel == TraversingLevel.CHANCE:
            if previousTypeOfLevel == TraversingLevel.MAX:
                nextTypeOfLevel = TraversingLevel.MIN
            else:
                nextTypeOfLevel = TraversingLevel.MAX

        return nextTypeOfLevel

    
    def makeTurnForBot(self, startingBoard):
        AIboard = AIboardState() # tutaj trzeba przepisac wszystkie pola i wtedy wywolywac
        AIboard = copy.deepcopy(startingBoard)
        AIboard.__diceI = randint(1,6)
        AIboard.__diceII = randint(1,6)
        currDepth = 0
        maxDepth = 5
        typeOfLevel = TraversingLevel.MAX
        previousTypeOfLevel = TraversingLevel.MAX
        self.maxMinChanceEvaluateState(AIboard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel)
        self.__moveI.AI.makeAImove(startingBoard)
        self.__moveII.AI.makeAImove(startingBoard)
