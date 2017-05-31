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
        self.setBestHeuristics()
        self._totalNumberOfMoves = 0

    def setBestHeuristics(self):
        self.theBestHeuristicForMoveI = -100000
        self.theBestHeuristicForMoveII = -100000
        self.theBestHeuristicForMoveIII = -100000
        self.theBestHeuristicForMoveIV = -100000


    def generateChildrenBoardStates(self, startingBoard):
        newNumberOfMoves = startingBoard._numberOfMoves
        if newNumberOfMoves > 0:
            if newNumberOfMoves == 1:
                return self.boardStatesFromDice(startingBoard, startingBoard._diceI, startingBoard._diceI, startingBoard._diceII, startingBoard._botMove._color)
            else:
                return self.boardStatesFromDice(startingBoard, startingBoard._diceII, startingBoard._diceI, startingBoard._diceII, startingBoard._botMove._color)
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


    def boardStatesFromDice(self, currBoard, diceNum, diceNumI, diceNumII, currColor):
        #generates all boardStates available: from currBoard using diceNumber roll( diceNumber == <1;6> )
        AIboards = []
        fieldIndex = 0
        bandFull = False
        if currColor == Color.BLACK and currBoard._blacksOnBand > 0:
            bandFull = True
            #print("Black banda")
        elif currColor == Color.RED and currBoard._redsOnBand > 0:
            bandFull = True
           # print("Red banda")

        if bandFull == False:#normal move
            for field in currBoard._fields_states:
                if currColor == field._color and field._is_empty == False:
                    newBoard = copy.deepcopy(currBoard)
                    newBoard._botMove = AImove(currColor, diceNum, diceNumI, diceNumII, fieldIndex, newBoard._numberOfMoves)
                    isValidMove = newBoard._botMove.makeTurn(newBoard, fieldIndex, currColor)
                    if isValidMove == True:
                        newBoard.AIbStateAfterMove() #calculated move and heuristic for one board in state
                        AIboards.append(newBoard)
                fieldIndex += 1
        else:
            #print("Generuje True")
            #checkers on band:
            newBoard = copy.deepcopy(currBoard)
            newBoard._botMove = AImove(currColor, diceNum, diceNumI, diceNumII, 0, currBoard._numberOfMoves)
            newBoard._botMove.removeFromBand(currColor, newBoard) # newBoard._botMove.removeFromBand(currColor, currBoard) -- JAK MOZNA !?????? currBoard ??? why :CCCC
            newBoard.AIbStateAfterMove()
            AIboards.append(newBoard)

        return AIboards


    def Astar(self, currBoard, currDepth):
        pass
    
    def greedyTraversing(self, currBoard, numberOfMoves):
        AIchildrenBoards = self.generateChildrenBoardStates(currBoard)
        currHeuristic = -100000
        moveIboard = currBoard
        #wybieramy pierwszy ruch
        for childBoard in AIchildrenBoards:
            if childBoard._heuristic > currHeuristic:
                currHeuristic = childBoard._heuristic
                self._moveI = copy.deepcopy(childBoard._botMove)
                moveIboard = childBoard
        # 2 ruch
        childrenBoards2 = self.generateChildrenBoardStates(moveIboard)
        currHeuristic = -100000
        moveIIboard = moveIboard
        for childBoard in childrenBoards2:
            if childBoard._heuristic > currHeuristic:
                currHeuristic = childBoard._heuristic
                self._moveII = copy.deepcopy(childBoard._botMove)
                moveIIboard = childBoard

        if numberOfMoves > 2:
            # 3 ruch
            childrenBoards3 = self.generateChildrenBoardStates(moveIIboard)
            currHeuristic = -100000
            moveIIIboard = moveIIboard
            for childBoard in childrenBoards3:
                if childBoard._heuristic > currHeuristic:
                    currHeuristic = childBoard._heuristic
                    self._moveIII = copy.deepcopy(childBoard._botMove)
                    moveIIIboard = childBoard
            # 4 ruch
            childrenBoards4 = self.generateChildrenBoardStates(moveIIIboard)
            currHeuristic = -100000
            for childBoard in childrenBoards4:
                if childBoard._heuristic > currHeuristic:
                    currHeuristic = childBoard._heuristic
                    self._moveIV = copy.deepcopy(childBoard._botMove)


    def Astar(self, currBoard):
        closedSet = []
        openSet = []

        if currBoard._numberOfMoves == 1:
            openSet = self.boardStatesFromDice(currBoard, currBoard._diceI, currBoard._diceI, currBoard._diceII, currBoard._botMove._color)
        else:
            openSet = self.boardStatesFromDice(currBoard, currBoard._diceII, currBoard._diceI, currBoard._diceII, currBoard._botMove._color) #zacznymay od drgueij kostki

        openSetHeuristic = []
        for AIboard in openSet:
            openSetHeuristic.append(AIboard._heuristic)

        while openSet:  # jesli lista niepusta
            maxHeur = max(openSetHeuristic)
            openSetHeuristic.remove(maxHeur)

            AIboardWithMaxHeuristic = None
            for AIboard in openSet:
                if AIboard._heuristic == maxHeur:
                    AIboardWithMaxHeuristic = AIboard
            openSet.remove(AIboardWithMaxHeuristic)

            if AIboardWithMaxHeuristic._numberOfMoves == 1:
                AIchildrenBoards = self.boardStatesFromDice(AIboardWithMaxHeuristic, AIboardWithMaxHeuristic._diceI, AIboardWithMaxHeuristic._diceI, AIboardWithMaxHeuristic._diceII, AIboardWithMaxHeuristic._botMove._color)
            else:
                AIchildrenBoards = self.boardStatesFromDice(AIboardWithMaxHeuristic, AIboardWithMaxHeuristic._diceII, AIboardWithMaxHeuristic._diceI, AIboardWithMaxHeuristic._diceII, AIboardWithMaxHeuristic._botMove._color)

            tentative_g_score = -1000
            theBestChildBoard = None
            for AIchildBoard in AIchildrenBoards:
                heuristic_between = AIchildBoard._heuristic - AIboardWithMaxHeuristic._heuristic
                if tentative_g_score < heuristic_between:
                    tentative_g_score = heuristic_between 
                    tentative_is_better = True 
                if tentative_is_better == True:
                    theBestChildBoard = AIchildBoard

            if theBestChildBoard != None:
                AIboardWithMaxHeuristic.f_score = AIboardWithMaxHeuristic._heuristic + theBestChildBoard._heuristic
            else:
                AIboardWithMaxHeuristic.f_score = AIboardWithMaxHeuristic._heuristic
            closedSet.append(AIboardWithMaxHeuristic)
        
        if AIboardWithMaxHeuristic != None:
            theReturningBoard = closedSet[0]
        else:
            theReturningBoard =  currBoard
        for AIboard in closedSet:
            if AIboard.f_score > theReturningBoard.f_score:
                theReturningBoard = AIboard

        return theReturningBoard


    def maxMinChanceEvaluateState(self, currBoard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel):
        if currDepth == maxDepth:
            return currBoard._heuristic
        
        AIchildrenBoards = self.generateChildrenBoardStates(currBoard)
        nextTypeOfLevel = self.setNextTraversingLevel(currBoard, typeOfLevel, previousTypeOfLevel)
        if typeOfLevel == TraversingLevel.MIN:
           # print("ETAP MIN")
            heuristic_V = 80000
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if heuristic < heuristic_V:
                    heuristic_V = heuristic
        elif typeOfLevel == TraversingLevel.MAX:
            #print(" <<<<<<ETAP MAX>>>>>>>>")
            heuristic_V = -100000
            for AIchildBoard in AIchildrenBoards:
                heuristic = self.maxMinChanceEvaluateState(AIchildBoard, currDepth + 1, maxDepth, nextTypeOfLevel, typeOfLevel)
                if heuristic > heuristic_V:
                    heuristic_V = heuristic
                    if self.theBestHeuristicForMoveIV < heuristic_V and currDepth == 3:
                        self._moveIV = copy.deepcopy(AIchildBoard._botMove)
                        self.theBestHeuristicForMoveIV =  heuristic_V
                       # print("moveIVIsBand : " + str(self._moveIV._isBandMove))
                    elif self.theBestHeuristicForMoveIII < heuristic_V and currDepth == 2:
                        self._moveIII = copy.deepcopy(AIchildBoard._botMove)
                        self.theBestHeuristicForMoveIII =  heuristic_V
                       # print("moveIIIsBand : " + str(self._moveIII._isBandMove))
                    elif self.theBestHeuristicForMoveII < heuristic_V and currDepth == 1:
                        self._moveII = copy.deepcopy(AIchildBoard._botMove)
                        self.theBestHeuristicForMoveII =  heuristic_V
                       # print("moveIIsBand : " + str(self._moveII._isBandMove))
                    elif self.theBestHeuristicForMoveI < heuristic_V and currDepth == 0: 
                        self._moveI = copy.deepcopy(AIchildBoard._botMove)
                       # print("moveIsBand : " + str(self._moveI._isBandMove))
                        self.theBestHeuristicForMoveI =  heuristic_V
        elif typeOfLevel == TraversingLevel.CHANCE:
            #print("ETAP CHANCE")
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
                self._moveI = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 4)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 3)
                self._moveIII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 2)
                self._moveIV = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1)
            elif ammountOfBlackOnBand == 1:
                self._moveI = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 3)
                self._moveIII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 2)
                self._moveIV = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1)
            elif ammountOfBlackOnBand == 2:
                self._moveI = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 3, True)
                self._moveIII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 2)
                self._moveIV = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1)       
            elif ammountOfBlackOnBand == 3:
                self._moveI = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 3, True)
                self._moveIII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 2, True)
                self._moveIV = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1)    
            elif ammountOfBlackOnBand == 4:
                self._moveI = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 4, True)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 3, True)
                self._moveIII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 2, True)
                self._moveIV = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1, True)    
        else:
            if ammountOfBlackOnBand == 0:
                self._moveI = AImove(Color.BLACK, diceNumII, diceNumI, diceNumII, 0, 2)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1)
            elif ammountOfBlackOnBand == 1:
                self._moveI = AImove(Color.BLACK, diceNumII, diceNumI, diceNumII, 0, 2, True)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1)
            elif ammountOfBlackOnBand == 2:
                self._moveI = AImove(Color.BLACK, diceNumII, diceNumI, diceNumII, 0, 2, True)
                self._moveII = AImove(Color.BLACK, diceNumI, diceNumI, diceNumII, 0, 1, True)


    def printData(self, currBoard):
        AIboard = AIboardState(AImove(Color.BLACK, 0, 0, 0, 0, 2), 0, currBoard)
        AIboard._heuristic = AIboard.calculateHeuristic()
        print(str(self._totalNumberOfMoves) + " " + str(AIboard._heuristic))
        self._totalNumberOfMoves += 1
    

    def setAIboard(self, AIboard, startingBoard, color, diceI, diceII, numberOfMoves):
        newAIboard = AIboardState(AImove(color, diceI, diceI, diceII, 0, numberOfMoves), 0, startingBoard) # tutaj trzeba przepisac wszystkie pola i wtedy wywolywac

        newAIboard._diceI = diceI
        newAIboard._diceII = diceII
        newAIboard._numberOfMoves = numberOfMoves
        newAIboard._botMove._amountOfMoves = numberOfMoves

        #self.setMoves(AIboard._blacksOnBand, AIboard._diceI, AIboard._diceII)

        return newAIboard


    def makeTurnForAstar(self, startingBoard, color):
        AIboard = AIboardState(AImove(color, 0, 0, 0, 0, 2), 0, startingBoard) 
        AIboard._diceI = randint(1,6)
        AIboard._diceII = randint(1,6)
      #  print("Kostka 1 " + str(AIboard._diceI))
        #print("Kostka 2 " + str(AIboard._diceII))
        if AIboard._diceI == AIboard._diceII:
            AIboard._numberOfMoves = 4
            AIboard._botMove._amountOfMoves = 4
            self._moveI = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 4)
            self._moveII = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 3) 
            self._moveIII = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 2)
            self._moveIV = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 1) 
        else:
            AIboard._numberOfMoves = 2
            AIboard._botMove._amountOfMoves = 2
            self._moveI = AImove(Color.BLACK, AIboard._diceII, AIboard._diceI, AIboard._diceII, 0, 2)
            self._moveII = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 1) 

        AIboard._botMove._currNum = AIboard._diceII

        AIboardI = self.Astar(AIboard)
        self._moveI = copy.deepcopy(AIboardI._botMove)
      #  print("moveI rusza z " + str(self._moveI._fieldNum) + " z kolorem: " + str(self._moveI._color) + " po kostce:  " + str(self._moveI._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveI._amountOfMoves) + "  dvizheniye po bandzje? " + str(self._moveI._isBandMove))
        self._moveI.makeAImove(startingBoard)
        self.printData(startingBoard)

        AIboard = self.setAIboard(AIboard, startingBoard, color, AIboard._diceI, AIboard._diceII, AIboard._numberOfMoves - 1)
        AIboardII = self.Astar(AIboard)
        self._moveII = copy.deepcopy(AIboardII._botMove)
       # print("moveII rusza z " + str(self._moveII._fieldNum) + " z kolorem: " + str(self._moveII._color) + " po kostce:  " + str(self._moveII._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveII._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveII._isBandMove))
        self._moveII.makeAImove(startingBoard)
        self.printData(startingBoard)

        if AIboard._diceI == AIboard._diceII:
            AIboard = self.setAIboard(AIboard, startingBoard, color, AIboard._diceI, AIboard._diceII, AIboard._numberOfMoves - 1)
            AIboardIII = self.Astar(AIboard)
            self._moveIII = copy.deepcopy(AIboardIII._botMove)
           # print("moveIII rusza z " + str(self._moveIII._fieldNum) + " z kolorem: " + str(self._moveIII._color) + " po kostce:  " + str(self._moveIII._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveIII._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveIII._isBandMove))
            self._moveIII.makeAImove(startingBoard)
            self.printData(startingBoard)

            AIboard = self.setAIboard(AIboard, startingBoard, color, AIboard._diceI, AIboard._diceII, AIboard._numberOfMoves - 1)
            AIboardIV = self.Astar(AIboard)
            self._moveIV = copy.deepcopy(AIboardIV._botMove)
          #  print("moveIV rusza z " + str(self._moveIV._fieldNum) + " z kolorem: " + str(self._moveIV._color) + " po kostce:  " + str(self._moveIV._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveIV._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveIV._isBandMove))
            self._moveIV.makeAImove(startingBoard)
            self.printData(startingBoard)


    def makeTurnForBot(self, startingBoard, color):
        self.setBestHeuristics()
        if startingBoard._blacksOnBand > 0:
            AIboard = AIboardState(AImove(color, 0, 0, 0, 0, 2), 0, startingBoard) # tutaj trzeba przepisac wszystkie pola i wtedy wywolywac
        else:
            AIboard = AIboardState(AImove(color, 0, 0, 0, 0, 2), 0, startingBoard) 
       # AIboard._botMove = AImove(Color.BLACK, 0)
        AIboard._diceI = randint(1,6)
        AIboard._diceII = randint(1,6)
        #print("Kostka 1 " + str(AIboard._diceI))
       # print("Kostka 2 " + str(AIboard._diceII))
        if AIboard._diceI == AIboard._diceII:
            AIboard._numberOfMoves = 4
            AIboard._botMove._amountOfMoves = 4
            self._moveI = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 4)
            self._moveII = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 3) 
            self._moveIII = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 2)
            self._moveIV = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 1) 
        else:
            AIboard._numberOfMoves = 2
            AIboard._botMove._amountOfMoves = 2
            self._moveI = AImove(Color.BLACK, AIboard._diceII, AIboard._diceI, AIboard._diceII, 0, 2)
            self._moveII = AImove(Color.BLACK, AIboard._diceI, AIboard._diceI, AIboard._diceII, 0, 1) 

        #self.setMoves(AIboard._blacksOnBand, AIboard._diceI, AIboard._diceII)
        AIboard._botMove._currNum = AIboard._diceII
        currDepth = 0
        maxDepth = 4
        
        
        typeOfLevel = TraversingLevel.MAX
        previousTypeOfLevel = TraversingLevel.MAX
        #self.greedyTraversing(AIboard, AIboard._numberOfMoves)
        self.maxMinChanceEvaluateState(AIboard, currDepth, maxDepth, typeOfLevel, previousTypeOfLevel)
       # print("WYSZEDL Z FUNKCJI    ")
       # print("moveI rusza z " + str(self._moveI._fieldNum) + " z kolorem: " + str(self._moveI._color) + " po kostce:  " + str(self._moveI._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveI._amountOfMoves) + "  dvizheniye po bandzje? " + str(self._moveI._isBandMove))
        self._moveI.makeAImove(startingBoard)
        self.printData(startingBoard)

        #print("moveII rusza z " + str(self._moveII._fieldNum) + " z kolorem: " + str(self._moveII._color) + " po kostce:  " + str(self._moveII._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveII._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveII._isBandMove))
        self._moveII.makeAImove(startingBoard)
        self._totalNumberOfMoves += 1
        self.printData(startingBoard)
        if AIboard._diceI == AIboard._diceII:
            self._moveIII.makeAImove(startingBoard)
            self._totalNumberOfMoves += 1
            self.printData(startingBoard)
            #print("moveIII rusza z " + str(self._moveIII._fieldNum) + " z kolorem: " + str(self._moveIII._color) + " po kostce:  " + str(self._moveIII._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveIII._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveIII._isBandMove))
            self._moveIV.makeAImove(startingBoard)
            self.printData(startingBoard)
           # print("moveIV rusza z " + str(self._moveIV._fieldNum) + " z kolorem: " + str(self._moveIV._color) + " po kostce:  " + str(self._moveIV._currNum) + " na rasza o pozostalych ruchach:  " + str(self._moveIV._amountOfMoves)+"  dvizheniye po bandzje? " + str(self._moveIV._isBandMove))
