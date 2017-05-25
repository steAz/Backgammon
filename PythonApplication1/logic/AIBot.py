
from enum import Enum
from logic.AImove import AImove
from model.AIboardState import AIboardState
from model.GameField import GameField
from model.GameField import Color
from random import randint
import copy
import sys

class TraversingLevel(Enum):
    MAX = 0
    MIN = 1
    CHANCE = 2

class AIbot(object):
    
    def __init__(self):
        self.__moveI = 0
        self.__moveII = 0


    def generateChildrenBoardStates(self, startingBoard):
        newNumberOfMoves = startingBoard._AIboardState__numberOfMoves
        if newNumberOfMoves > 0:
            if newNumberOfMoves == 1:
                return self.boardStatesFromDice(startingBoard, startingBoard._AIboardState__diceI, startingBoard._AIboardState__botMove._AImove__color)
            else:
                return self.boardStatesFromDice(startingBoard, startingBoard._AIboardState__diceII, startingBoard._AIboardState__botMove._AImove__color)
        else:
            AIboards = []
            #generating new boards with new dice roll (CHANCE level)
            for i in range(1, 7):
                for j in range(i, 7):
                    newBoard = copy.deepcopy(startingBoard)
                    newBoard._AIboardState__diceI = i
                    newBoard._AIboardState__diceII = j
                    if i != j: 
                        newBoard._AIboardState__numberOfMoves = 2
                    else:
                         newBoard._AIboardState__numberOfMoves = 4
                    AIboards.append(newBoard)
            return Aiboards


    def boardStatesFromDice(self, currBoard, diceNum, currColor):
        #generates all boardStates available: from currBoard using diceNumber roll( diceNumber == <1;6> )
        AIboards = []
        fieldIndex = 0
        for field in currBoard._AIboardState__fields_states:
            if currColor == field._GameField__color and field._GameField__is_empty == False:
                newBoard = copy.deepcopy(currBoard)
                newBoard._AIboardState__botMove = AImove(currColor, diceNum, fieldIndex)
                isValidMove = newBoard._AIboardState__botMove.makeTurn(newBoard, fieldIndex, currColor)
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
                    heuristic_V = newBoard._AIboardState__heuristic
                    if currDepth == 2:
                        self.__moveII = newBoard._AIboardState__botMove
                    elif currDepth == 1:
                        self.__moveI = newBoard._AIboardState__botMove
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
        AIboard = AIboardState(startingBoardState = startingBoard) # tutaj trzeba przepisac wszystkie pola i wtedy wywolywac
        AIboard._AIboardState__botMove = AImove(color = Color.BLACK)
        AIboard._AIboardState__diceI = randint(1,6)
        AIboard._AIboardState__diceII = randint(1,6)
        if AIboard._AIboardState__diceI == AIboard._AIboardState__diceII:
            AIboard._AIboardState__numberOfMoves = 4
        else:
            AIboard._AIboardState__numberOfMoves = 2
        currDepth = 0
        maxDepth = 5
        typeOfLevel = TraversingLevel.MAX
        previousTypeOfLevel = TraversingLevel.MAX
        self.maxMinChanceEvaluateState(AIboard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel)
        self.__moveI.makeAImove(startingBoard)
        self.__moveII.makeAImove(startingBoard)
