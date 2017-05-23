from tkinter import *
from random import randint
from model.GameField import *


class Game:
    @property
    def player(self):
        return self.__player

    def __init__(self):
        self.__isRandomized = False
        self.__isDiceChosen = False
        self.__labelDiceI = None
        self.__labelDiceII = None
        self.__currNumI = None
        self.__currNumII = None
        self.__currNum = None
        self.__amountOfMoves = None
        self.__redsOnBand = 0
        self.__blacksOnBand = 0

    @player.setter
    def player(self, player):
        self.__player = player

    def setRandNumbers(self, event=None):
        
        if self.__isRandomized == False:
            self.__isDiceChosen = False
            numI = randint(1,6)
            numII=randint(1,6)
            self.__isRandomized = True
            self.displayRandNumbers(numI, numII)
            self.__currNumI = numI
            self.__currNumII = numII

            if numI == numII:
                self.__amountOfMoves = 4
            else:
                self.__amountOfMoves = 2
        
    def displayRandNumbers(self, numI, numII):
        if self.__isRandomized:
            self.__labelDiceI = Label(text=str(numI))
            self.__labelDiceII = Label(text=str(numII))
            self.__labelDiceI.place(x = 20,y = 430)
            self.__labelDiceII.place(x = 35,y = 430)

    def makeTurn(self, board, fieldNum, currentColor):
        if self.isValidMove(fieldNum, currentColor, board) == False:
            return False
        if currentColor == Color.RED:
            destNumber = fieldNum - self.__currNum
            isRed = True
        else:
            destNumber = fieldNum + self.__currNum
            isBlack = False

        destField = board._BoardState__fields_states[destNumber]
        currField = board._BoardState__fields_states[fieldNum]
        if destField.is_empty == True:
            self.moveToEmpty(destField, currField)
            return True
        if destField.color == currField.color:
            self.moveToOur(destField, currField)
            return True
        elif destField.color != currentColor and destField.number_of_checkers == 1:
            self.hitEnemy(destField, currField)
       
        

        
    def isEverythingAtHome(self,  board, currentColor):
        amountOfCheckersAtHome = 0
        if currentColor == Color.RED:
            for i in range(6):
                if board._BoardState__fields_states[i].color == currentColor:
                    amountOfCheckersAtHome += board._BoardState__fields_states[i].number_of_checkers
            if amountOfCheckersAtHome == 15:
                return True
            else:
                return False
        else:
            for i in range(6):
                if board._BoardState__fields_states[i + 18].color == currentColor:
                    amountOfCheckersAtHome += board._BoardState__fields_states[i + 18].number_of_checkers
            if amountOfCheckersAtHome == 15:
                return True
            else:
                return False


    def setDice(self,  numOfDice = 0, event=None):
        if self.__amountOfMoves != 1: # when we're not allowed to change dice
            self.__isDiceChosen = True
            if numOfDice == 1:
                self.__labelDiceI.configure(foreground="red")
                self.__labelDiceII.configure(foreground="black")
                self.__currNum = self.__currNumI
            else:
                self.__labelDiceII.configure(foreground="red")
                self.__labelDiceI.configure(foreground="black")
                self.__currNum = self.__currNumII

    #moving to empty field
    def moveToEmpty(self, destField, currField):
        destField.is_empty = False
        destField.number_of_checkers = 1
        destField.color = currField.color
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True

    def moveToCourt(self, currField):
        pass
            

    def moveToOur(self, destField, currField):
        destField.number_of_checkers += 1
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True

    def hitEnemy(self, destField, currField):
        currField.number_of_checkers -= 1
        destField.color = currField.color
        if destField.color == Color.BLACK:
            self.__redsOnBand += 1
        else:
            self.__blacksOnBand += 1

        if currField.number_of_checkers == 0:
            currField.is_empty = True
        

    # method returns true if we can move checker from fieldNumber by self.__currNum positions
    def isValidMove(self, fieldNumber, playerColor, board):
        if playerColor == Color.RED:
            destNumber = fieldNumber - self.__currNum
        else:
            destNumber = fieldNumber + self.__currNum

        if destNumber > 23 or destNumber < 0:
            return False
        destField = board._BoardState__fields_states[destNumber]

        if destField.color != playerColor and destField.number_of_checkers > 1:
            return False
        
        return True

        
    @property
    def currDice(self):
        return self.__currNum

    @property
    def isRandomized(self):
        return self.__isRandomized

    @property
    def isDiceChosen(self):
        return self.__isDiceChosen

    @isDiceChosen.setter
    def isDiceChosen(self, new_amount):
        self.__isDiceChosen = new_amount

    @isRandomized.setter
    def isRandomized(self, new_amount):
        self.__isRandomized = new_amount