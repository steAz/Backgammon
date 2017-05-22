from tkinter import *
from random import randint


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

    @player.setter
    def player(self, player):
        self.__player = player

    def setRandNumbers(self, event=None):
        if self.__isRandomized == False:
            numI = randint(1,6)
            numII=randint(1,6)
            self.__isRandomized = True
            self.displayRandNumbers(numI, numII)
            self.__currNumI = numI
            self.__currNumII = numII
        
    def displayRandNumbers(self, numI, numII):
        if self.__isRandomized:
            self.__labelDiceI = Label(text=str(numI))
            self.__labelDiceII = Label(text=str(numII))
            self.__labelDiceI.place(x = 20,y = 430)
            self.__labelDiceII.place(x = 35,y = 430)

    def makeTurn(self, board, fieldNum, currentColor):
        if self.isValidMove(fieldNum, currentColor, board) == False:
            return
        if playerColor == Color.RED:
            destNumber = fieldNumber - self.__currNum
        else:
            destNumber = fieldNumber + self.__currNum
        destField = board._BoardState__fields_states[destNumber]


        


    def setDice(self,  numOfDice = 0, event=None):
        if numOfDice == 1:
            self.__labelDiceI.configure(foreground="red")
            self.__labelDiceII.configure(foreground="black")
            self.__currNum = self.__curNummI
        else:
            self.__labelDiceII.configure(foreground="red")
            self.__labelDiceI.configure(foreground="black")
            self.__currNum = self.__curNummII

    #moving to empty field
    def moveToEmpty(self, board, destField, currColor):
        board._BoardState__fields_states[destNumber].is_empty = False


    # method returns true if we can move checker from fieldNumber by self.__currNum positions
    def isValidMove(self, fieldNumber, playerColor, boardState):
        if playerColor == Color.RED:
            destNumber = fieldNumber - self.__currNum
        else:
            destNumber = fieldNumber + self.__currNum

        if destNumber > 23 or destNumber < 0:
            return False
        destField = boardState._BoardState__fields_states[destNumber]

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



#currField = board._BoardState__fields_states[fieldNum]
#        destinationNum = fieldNum - self.__currNum
#        if destinationNum >= 0: # 24 fields
#          #  destinationField = board._BoardState__fields_states[destinationNum] 
#            if destinationField.is_empty == True:
#                board._BoardState__fields_states[destinationNum].is_empty = False
#                destinationField.number_of_checkers = 1
#                destinationField.color = Color.RED
#            elif destinationField.color == Color.RED:
#                destinationField.number_of_checkers += 1
#            elif destinationField.color == Color.BLACK and destinationField.number_of_checkers == 1:
#                destinationField.color = Color.RED
#elif destinationNum < 0:
 #           print("Nie mozesz poruszyc sie tym krazkiem")