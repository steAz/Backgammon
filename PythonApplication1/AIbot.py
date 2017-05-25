from enum import Enum
from AImove import AImove
from AIboardState import AIboardState
from GameField import GameField
from GameField import Color
from random import randint
import copy
import sys

class TraversingLevel(Enum):
    MAX = 0
    MIN = 1
    CHANCE = 2

class AIbot(object):
    
    def __init__(self):
        self._moveI = AImove(Color.BLACK, 0, 0, 2)
        self._moveII = AImove(Color.BLACK, 0, 0, 1)


    def generateChildrenBoardStates(self, startingBoard):
        newNumberOfMoves = startingBoard._numberOfMoves
        if newNumberOfMoves > 0:
            if newNumberOfMoves == 1:
                return self.boardStatesFromDice(startingBoard, startingBoard._diceI, startingBoard._botMove._color)
            else:
                return self.boardStatesFromDice(startingBoard, startingBoard._diceII, startingBoard._botMove._color)
        else:
            AIboards = []
            #generating new boards with new dice roll (CHANCE level)
            for i in range(1, 7):
                for j in range(i, 7):
                    newBoard = copy.deepcopy(startingBoard)
                    newBoard._diceI = i
                    newBoard._diceII = j
                    newBoard._botMove._currNum = j
                    if startingBoard._botMove._color == Color.RED:
                        newBoard._botMove._color = Color.BLACK
                    elif startingBoard._botMove._color == Color.BLACK:
                        newBoard._botMove._color = Color.RED
                    if i != j: 
                        newBoard._numberOfMoves = 2
                        newBoard._botMove._amountOfMoves = 2
                    else:
                         newBoard._numberOfMoves = 4
                         newBoard._botMove._amountOfMoves = 4
                    AIboards.append(newBoard)
            return AIboards


    def boardStatesFromDice(self, currBoard, diceNum, currColor):
        #generates all boardStates available: from currBoard using diceNumber roll( diceNumber == <1;6> )
        AIboards = []
        fieldIndex = 0
        for field in currBoard._fields_states:
            if currColor == field._color and field._is_empty == False:
                newBoard = copy.deepcopy(currBoard)
                newBoard._botMove = AImove(currColor, diceNum, fieldIndex, newBoard._numberOfMoves)
                isValidMove = newBoard._botMove.makeTurn(newBoard, fieldIndex, currColor)
                if isValidMove == True:
                    newBoard.AIbStateAfterMove() #calculated move and heuristic for one board in state
                    AIboards.append(newBoard)
            fieldIndex += 1

        return AIboards


    def maxMinChanceEvaluateState(self, currBoard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel):
        if currDepth == maxDepth:
            return currBoard._heuristic
        
        AIchildrenBoards = self.generateChildrenBoardStates(currBoard)
        nextTypeOfLevel = self.setNextTraversingLevel(currBoard, typeOfLevel, previousTypeOfLevel)
        if typeOfLevel == TraversingLevel.MIN:
            print("ETAP MIN")
            heuristic_V = 32767
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if heuristic < heuristic_V:
                    heuristic_V = heuristic
        elif typeOfLevel == TraversingLevel.MAX:
            print(" <<<<<<ETAP MAX>>>>>>>>")
            heuristic_V = -32767
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if heuristic > heuristic_V:
                    heuristic_V = heuristic
                    if currDepth == 1:
                        self._moveII = copy.deepcopy(AIchildBoard._botMove)
                    elif currDepth == 0:
                        self._moveI = copy.deepcopy(AIchildBoard._botMove)
        elif typeOfLevel == TraversingLevel.CHANCE:
            print("ETAP CHANCE")
            heuristic_V = 0 
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                probabilityOfAIchildBoard = 1/21
                heuristic_V += probabilityOfAIchildBoard * heuristic
               
        return heuristic_V


    def setNextTraversingLevel(self, currBoard, typeOfLevel, previousTypeOfLevel):
        if typeOfLevel == TraversingLevel.MIN:
            if currBoard._numberOfMoves == 1:
                    nextTypeOfLevel = TraversingLevel.CHANCE
            else:
                    nextTypeOfLevel = TraversingLevel.MIN
        elif typeOfLevel == TraversingLevel.MAX:
            if currBoard._numberOfMoves == 1:
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
        AIboard = AIboardState(AImove(Color.BLACK, 0, 0, 2), 0, startingBoard) # tutaj trzeba przepisac wszystkie pola i wtedy wywolywac
       # AIboard._botMove = AImove(Color.BLACK, 0)
        AIboard._diceI = randint(1,6)
        AIboard._diceII = randint(1,6)
        if AIboard._diceI == AIboard._diceII:
            AIboard._numberOfMoves = 4
            AIboard._botMove._amountOfMoves = 4
        else:
            AIboard._numberOfMoves = 2
            AIboard._botMove._amountOfMoves = 2
        AIboard._botMove._currNum = AIboard._diceII
        currDepth = 0
        maxDepth = 5
        typeOfLevel = TraversingLevel.MAX
        previousTypeOfLevel = TraversingLevel.MAX
        self.maxMinChanceEvaluateState(AIboard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel)
        print("WYSZEDL Z FUNKCJI")
        print("moveI rusza z " + str(self._moveI._fieldNum) + "z kolorem: " + str(self._moveI._color) + "o kostce:  " + str(self._moveI._currNum) + "o pozostalych ruchach:  " + str(self._moveI._amountOfMoves))
        self._moveI.makeAImove(startingBoard)
        print("moveII rusza z " + str(self._moveII._fieldNum) + "z kolorem: " + str(self._moveII._color) + "o kostce:  " + str(self._moveII._currNum) + "o pozostalych ruchach:  " + str(self._moveII._amountOfMoves))
        self._moveII.makeAImove(startingBoard)
