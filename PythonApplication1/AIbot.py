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
        self.theBestHeuristicForMoveI = -100000
        self.theBestHeuristicForMoveII = -100000
        self.theBestHeuristicForMoveIII = -100000
        self.theBestHeuristicForMoveIV = -100000
        pass


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
        bandFull = False
        if currColor == Color.BLACK and currBoard._blacksOnBand > 0:
            bandFull = True
            print("Black banda")
        elif currColor == Color.RED and currBoard._redsOnBand > 0:
            bandFull = True
            print("Red banda")

        if bandFull == False:#normal move
            for field in currBoard._fields_states:
                if currColor == field._color and field._is_empty == False:
                    newBoard = copy.deepcopy(currBoard)
                    newBoard._botMove = AImove(currColor, diceNum, fieldIndex, newBoard._numberOfMoves)
                    isValidMove = newBoard._botMove.makeTurn(newBoard, fieldIndex, currColor)
                    if isValidMove == True:
                        newBoard.AIbStateAfterMove() #calculated move and heuristic for one board in state
                        AIboards.append(newBoard)
                fieldIndex += 1
        else:
            print("Generuje True")
            #checkers on band:
            newBoard = copy.deepcopy(currBoard)
            newBoard._botMove = AImove(currColor, diceNum, 0, currBoard._numberOfMoves)
            newBoard._botMove.removeFromBand(currColor, newBoard) # newBoard._botMove.removeFromBand(currColor, currBoard) -- JAK MOZNA !?????? currBoard ??? why :CCCC
            newBoard.AIbStateAfterMove()
            AIboards.append(newBoard)

        return AIboards


    def Astar(self, currBoard, currDepth):
        pass


    def maxMinChanceEvaluateState(self, currBoard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel):
        if currDepth == maxDepth:
            return currBoard._heuristic
        
        AIchildrenBoards = self.generateChildrenBoardStates(currBoard)
        nextTypeOfLevel = self.setNextTraversingLevel(currBoard, typeOfLevel, previousTypeOfLevel)
        if typeOfLevel == TraversingLevel.MIN:
            print("ETAP MIN")
            heuristic_V = 80000
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if heuristic < heuristic_V:
                    heuristic_V = heuristic
        elif typeOfLevel == TraversingLevel.MAX:
            print(" <<<<<<ETAP MAX>>>>>>>>")
            heuristic_V = -100000
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if heuristic > heuristic_V:
                    heuristic_V = heuristic
                    if self.theBestHeuristicForMoveIV < heuristic_V and currDepth == 3:
                        self._moveIV = copy.deepcopy(AIchildBoard._botMove)
                        self.theBestHeuristicForMoveIV =  heuristic_V
                        print("moveIVIsBand : " + str(self._moveIV._isBandMove))
                    elif self.theBestHeuristicForMoveIII < heuristic_V and currDepth == 2:
                        self._moveIII = copy.deepcopy(AIchildBoard._botMove)
                        self.theBestHeuristicForMoveIII =  heuristic_V
                        print("moveIIIsBand : " + str(self._moveIII._isBandMove))
                    elif self.theBestHeuristicForMoveII < heuristic_V and currDepth == 1:
                        self._moveII = copy.deepcopy(AIchildBoard._botMove)
                        self.theBestHeuristicForMoveII =  heuristic_V
                        print("moveIIsBand : " + str(self._moveII._isBandMove))
                    elif self.theBestHeuristicForMoveI < heuristic_V and currDepth == 0: 
                        self._moveI = copy.deepcopy(AIchildBoard._botMove)
                        print("moveIsBand : " + str(self._moveI._isBandMove))
                        self.theBestHeuristicForMoveI =  heuristic_V
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

    def setMoves(self, ammountOfBlackOnBand, diceNumI, diceNumII):
        if diceNumI == diceNumII:
            isDouble = True
        else:
            isDouble = False

        if isDouble:
            if ammountOfBlackOnBand == 0:
                self._moveI = AImove(Color.BLACK, diceNumI, 0, 4)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 3)
                self._moveIII = AImove(Color.BLACK, diceNumI, 0, 2)
                self._moveIV = AImove(Color.BLACK, diceNumI, 0, 1)
            elif ammountOfBlackOnBand == 1:
                self._moveI = AImove(Color.BLACK, diceNumI, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 3)
                self._moveIII = AImove(Color.BLACK, diceNumI, 0, 2)
                self._moveIV = AImove(Color.BLACK, diceNumI, 0, 1)
            elif ammountOfBlackOnBand == 2:
                self._moveI = AImove(Color.BLACK, diceNumI, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 3, True)
                self._moveIII = AImove(Color.BLACK, diceNumI, 0, 2)
                self._moveIV = AImove(Color.BLACK, diceNumI, 0, 1)       
            elif ammountOfBlackOnBand == 3:
                self._moveI = AImove(Color.BLACK, diceNumI, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 3, True)
                self._moveIII = AImove(Color.BLACK, diceNumI, 0, 2, True)
                self._moveIV = AImove(Color.BLACK, diceNumI, 0, 1)    
            elif ammountOfBlackOnBand == 4:
                self._moveI = AImove(Color.BLACK, diceNumI, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 3, True)
                self._moveIII = AImove(Color.BLACK, diceNumI, 0, 2, True)
                self._moveIV = AImove(Color.BLACK, diceNumI, 0, 1, True)    
        else:
            if ammountOfBlackOnBand == 0:
                self._moveI = AImove(Color.BLACK, diceNumII, 0, 2)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 1)
            elif ammountOfBlackOnBand == 1:
                self._moveI = AImove(Color.BLACK, diceNumII, 0, 2, True)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 1)
            elif ammountOfBlackOnBand == 2:
                self._moveI = AImove(Color.BLACK, diceNumII, 0, 2, True)
                self._moveII = AImove(Color.BLACK, diceNumI, 0, 1, True) 
    
    
    def makeTurnForBot(self, startingBoard, color):
        if startingBoard._blacksOnBand > 0:
            AIboard = AIboardState(AImove(color, 0, 0, 2), 0, startingBoard) # tutaj trzeba przepisac wszystkie pola i wtedy wywolywac
        else:
            AIboard = AIboardState(AImove(color, 0, 0, 2), 0, startingBoard) 
       # AIboard._botMove = AImove(Color.BLACK, 0)
        AIboard._diceI = randint(1,6)
        AIboard._diceII = randint(1,6)
        print("Kostka 1 " + str(AIboard._diceI))
        print("Kostka 2 " + str(AIboard._diceII))
        if AIboard._diceI == AIboard._diceII:
            AIboard._numberOfMoves = 4
            AIboard._botMove._amountOfMoves = 4
            self._moveI = AImove(Color.BLACK, AIboard._diceI, 0, 4)
            self._moveII = AImove(Color.BLACK, AIboard._diceI, 0, 3) 
            self._moveIII = AImove(Color.BLACK, AIboard._diceI, 0, 2)
            self._moveIV = AImove(Color.BLACK, AIboard._diceI, 0, 1) 
        else:
            AIboard._numberOfMoves = 2
            AIboard._botMove._amountOfMoves = 2
            self._moveI = AImove(Color.BLACK, AIboard._diceII, 0, 2)
            self._moveII = AImove(Color.BLACK, AIboard._diceI, 0, 1) 

        #self.setMoves(AIboard._blacksOnBand, AIboard._diceI, AIboard._diceII)
        AIboard._botMove._currNum = AIboard._diceII
        currDepth = 0
        maxDepth = 2
        
        
        typeOfLevel = TraversingLevel.MAX
        previousTypeOfLevel = TraversingLevel.MAX
        self.maxMinChanceEvaluateState(AIboard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel)
        print("WYSZEDL Z FUNKCJI    ")
        print("moveI rusza z " + str(self._moveI._fieldNum) + " z kolorem: " + str(self._moveI._color) + " po kostce:  " + str(self._moveI._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveI._amountOfMoves) + "  dvizheniye po bandzje? " + str(self._moveI._isBandMove))
        self._moveI.makeAImove(startingBoard)
        print("moveII rusza z " + str(self._moveII._fieldNum) + " z kolorem: " + str(self._moveII._color) + " po kostce:  " + str(self._moveII._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveII._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveII._isBandMove))
        self._moveII.makeAImove(startingBoard)
        if AIboard._diceI == AIboard._diceII:
            self._moveIII.makeAImove(startingBoard)
            print("moveIII rusza z " + str(self._moveIII._fieldNum) + " z kolorem: " + str(self._moveIII._color) + " po kostce:  " + str(self._moveIII._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveIII._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveIII._isBandMove))
            self._moveIV.makeAImove(startingBoard)
            print("moveIV rusza z " + str(self._moveIV._fieldNum) + " z kolorem: " + str(self._moveIV._color) + " po kostce:  " + str(self._moveIV._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveIV._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveIV._isBandMove))




            # TODO : NIE MOZNA TRACIC RUCHU PO WYJSCIU Z BANDY I ZLE WYBRANEJ KOSTCE PRZY 6