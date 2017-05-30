from tkinter import *
from random import randint
from GameField import *
from BoardState import BoardState


class Game:
    @property
    def player(self):
        return self._player

    def __init__(self):
        self._isRandomized = False
        self._isDiceChosen = False
        self._labelDiceI = None
        self._labelDiceII = None
        self._currNumI = None
        self._currNumII = None
        self._currNum = None
        self._amountOfMoves = None

    @player.setter
    def player(self, player):
        self._player = player


    def setRandNumbers(self, event=None):
        if self._isRandomized == False:
            self._isDiceChosen = False
            numI = randint(1,6)
            numII=randint(1,6)
            self._isRandomized = True
            self.displayRandNumbers(numI, numII)
            self._currNumI = numI
            self._currNumII = numII

            if numI == numII:
                self._amountOfMoves = 4
            else:
                self._amountOfMoves = 2
        

    def displayRandNumbers(self, numI, numII):
        if self._isRandomized:
            self._labelDiceI = Label(text=str(numI))
            self._labelDiceII = Label(text=str(numII))
            self._labelDiceI.place(x = 20,y = 430)
            self._labelDiceII.place(x = 35,y = 430)


    def makeTurn(self, board, fieldNum, currentColor):  # return True means that move has passed
        isNormalValidation = True
        if self.isEverythingAtHome(board, currentColor) == True:
            print("isEverythingAtHome")
            isNormalValidation = False

        if isNormalValidation == True:
            if self.isValidMove(fieldNum, currentColor, board) == False:
                return False
            return self.normalMove(board, fieldNum, currentColor)
        else: 
            return self.homeMove(board, fieldNum, currentColor)

    
    def homeIndexes(self, color):
        if color == Color.RED:
            return range(6)
        else:
            return range(18,24)
          

    def isAnotherFieldsToTheCourt(self, fieldNum, playerColor, board, isLastMove=True):
        if isLastMove == True:
            secondDice = self._currNum
        elif self._currNum == self._currNumI:
            secondDice = self._currNumII
        else:
            secondDice = self._currNumI
            
        for i in self.homeIndexes(playerColor):
            if i != fieldNum:
                if self.fieldsToTheCourt(playerColor, i) == self._currNum or self.fieldsToTheCourt(playerColor, i) == secondDice:
                    field = board._fields_states[i]
                    if field.is_empty == False and field.color == playerColor:
                        return True
        return False

    def isAnotherFurther(self, fieldNum, playerColor, board):
        for i in self.homeIndexes(playerColor):
            if i != fieldNum:
                if self.fieldsToTheCourt(playerColor, i) > self.fieldsToTheCourt(playerColor, fieldNum):
                   # print("I")
                    if self.isFieldInTheSameColor(i, playerColor, board) == True:
                        #print("numer:  " + str(i)  + str(board._fields_states[i].is_empty))
                        return True
        return False

    def isFieldInTheSameColor(self, fieldNum, playerColor, board):
        field = board._fields_states[fieldNum]
        if field.is_empty == False and field.color == playerColor:
            return True
        else:
            return False

    def homeMove(self, board, fieldNum, playerColor):
        if playerColor == Color.RED:
            destNumber = fieldNum - self._currNum
        else:
            destNumber = fieldNum + self._currNum
        destField = board._fields_states[destNumber]

        if self._amountOfMoves == 1: #jesli jest to ostatni ruch
            if self.fieldsToTheCourt(playerColor, fieldNum) == self._currNum:   #jesli nasza pozycja jest na pozycji wybranej kostki, to wyjdz na dwor
                self.moveToTheCourt(fieldNum, playerColor, board)
                return True
            elif self.isAnotherFieldsToTheCourt(fieldNum, playerColor, board) == True:
                print("isAnotherFieldsToTheCourt")
                return False
            elif self.isAnotherFurther(fieldNum, playerColor, board) == True: 
                print("isAnotherFurther")
                return False
            elif destNumber <= 23 and destNumber >= 0:
                field = board._fields_states[fieldNum]
                return self.moveCheckerStandard(destField, field, playerColor, board) # make normal move
            else:
                self.moveToTheCourt(fieldNum, playerColor, board)
                return True
        else: # jesli zostal jeszcze jeden ruch, albo wiecej przy dublecie
            if self.fieldsToTheCourt(playerColor, fieldNum) == self._currNumI or self.fieldsToTheCourt(playerColor, fieldNum) == self._currNumII:
                #chosen field is correct (distance to court equals dice's roll)
                if self.fieldsToTheCourt(playerColor, fieldNum) == self._currNum:
                    self.moveToTheCourt(fieldNum, playerColor, board)
                    return True
                elif destNumber <= 23 and destNumber >= 0:
                    field = board._fields_states[fieldNum]
                    return self.moveCheckerStandard(destField, field, playerColor, board) # make normal move
                else:
                    self.moveToTheCourt(fieldNum, playerColor, board)
                    return True
            else:
                if self.isAnotherFieldsToTheCourt(fieldNum, playerColor, board, False) == True: # szukamy czy inne pole jest rowne ktorejs z 2 kostek
                    print("isAnotherFieldsToTheCourt_2")
                    return False
                elif self.isAnotherFurther(fieldNum, playerColor, board) == True:
                    print("isAnotherFurther_2")
                    return False
                elif destNumber <= 23 and destNumber >= 0:
                    field = board._fields_states[fieldNum]
                    return self.moveCheckerStandard(destField, field, playerColor, board) # make normal move
                else:
                    self.moveToTheCourt(fieldNum, playerColor, board)
                    return True


    def fieldsToTheCourt(self, currColor, fieldNum):
        if currColor == Color.RED:
            return fieldNum + 1
        else:
            return 24 - fieldNum 

    def moveToTheCourt(self, fieldNum, playerColor, board):
        print("movetoTheCOurt called")
        if playerColor == Color.RED:
            board._redsOnTheCourt += 1
        else:
            board._blacksOnTheCourt += 1

        field =  board._fields_states[fieldNum]
        field.number_of_checkers -= 1
        if field.number_of_checkers == 0:
            field.is_empty = True 
        
    # method returns true if we can move checker from fieldNumber by self._currNum positions ## IT DOESTN CHECK THE HOME VALIDATION WHEN PLAYER WANTS TO WIN ##
    def isValidMove(self, fieldNumber, playerColor, board):
        if playerColor == Color.RED:
            destNumber = fieldNumber - self._currNum
        else:
            destNumber = fieldNumber + self._currNum

        if destNumber > 23 or destNumber < 0:
            return False
        destField = board._fields_states[destNumber]

        if destField.color != playerColor and destField.number_of_checkers > 1:
            return False
        
        return True

        
    def normalMove(self, board, fieldNum, currentColor):
        if currentColor == Color.RED:
            destNumber = fieldNum - self._currNum
            isRed = True
        else:
            destNumber = fieldNum + self._currNum
            isBlack = False

        destField = board._fields_states[destNumber]
        currField = board._fields_states[fieldNum]
        return self.moveCheckerStandard(destField, currField, currentColor, board) # make normal move


    def moveCheckerStandard(self, destField, currField, currColor, board):   
        if destField.is_empty == True:
            self.moveToEmpty(destField, currField)
            return True
        if destField.color == currField.color:
            self.moveToOur(destField, currField)
            return True
        elif destField.color != currColor and destField.number_of_checkers == 1:
            self.hitEnemy(destField, currField, board)
            return True
        else:
            print("move checker standard")
            return False

        
    def isEverythingAtHome(self,  board, currentColor):
        amountOfCheckersAtHome = 0
        if currentColor == Color.RED:
            for i in range(18):
                if board._fields_states[i + 6].color == currentColor and board._fields_states[i + 6].is_empty == False:
                    return False    #amountOfCheckersOutOfHome += board._fields_states[i + 5].number_of_checkers
            if board._redsOnBand > 0:
                return False
            else:
                return True
        else:
            for i in range(18):
                if board._fields_states[i].color == currentColor and board._fields_states[i].is_empty == False:
                    return False    #amountOfCheckersOutOfHome += board._fields_states[i + 5].number_of_checkers
            if board._blacksOnBand > 0:
                return False
            else:
                return True


    def setDice(self,  numOfDice = 0, event=None):
        if self._amountOfMoves != 1: # when we're not allowed to change dice
            self._isDiceChosen = True
            if numOfDice == 1:
                self._labelDiceI.configure(foreground="red")
                self._labelDiceII.configure(foreground="black")
                self._currNum = self._currNumI
            else:
                self._labelDiceII.configure(foreground="red")
                self._labelDiceI.configure(foreground="black")
                self._currNum = self._currNumII

    #moving to empty field
    def moveToEmpty(self, destField, currField):
        destField.is_empty = False
        destField.number_of_checkers = 1
        destField.color = currField.color
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True

    def moveToEmptyFromBand(self, destField, currColor, board):
        destField.is_empty = False
        destField.number_of_checkers = 1
        destField.color = currColor
        if currColor == Color.RED:
            board._redsOnBand -= 1
        else:
            board._blacksOnBand -=1
            

    def moveToOur(self, destField, currField):
        destField.number_of_checkers += 1
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True


    def moveToOurFromBand(self, destField, currColor, board):
        destField.number_of_checkers += 1
        if currColor == Color.RED:
            board._redsOnBand -= 1
        else:
            board._blacksOnBand -= 1


    def hitEnemy(self, destField, currField, board):
        currField.number_of_checkers -= 1
        destField.color = currField.color
        if destField.color == Color.BLACK:
            board._redsOnBand += 1
        else:
            board._blacksOnBand += 1

        if currField.number_of_checkers == 0:
            currField.is_empty = True

    def hitEnemyFromBand(self, destField, currColor, board):
        destField.number_of_checkers = 1
        destField.color = currColor
        if currColor == Color.RED:
            board._redsOnBand -= 1
            board._blacksOnBand += 1
        else:
            board._blacksOnBand -=1
            board._redsOnBand += 1

    def removeFromBand(self, currColor, board):
        if currColor == Color.RED:
            destField = board._fields_states[24 - self._currNum]
        else:
            destField = board._fields_states[self._currNum - 1]

        if destField.is_empty == True:
            print("empty")
            self.moveToEmptyFromBand(destField, currColor, board)
        elif destField.color == currColor:
            print("our")
            self.moveToOurFromBand(destField, currColor, board)
        elif destField.number_of_checkers == 1:
            self.hitEnemyFromBand(destField, currColor, board)
        else:
            # there are more than 1 enemy checker on the destination field
            pass

    def ableToEscapeBand(self, currColor, board):
        if currColor == Color.RED:
            destField1 = board._fields_states[24 - self._currNumI]
            destField2 = board._fields_states[24 - self._currNumII]
        else:
            destField1 = board._fields_states[self._currNumI - 1]
            destField2 = board._fields_states[self._currNumII - 1]
        if destField1.is_empty == False and destField1.color != currColor and destField1.number_of_checkers > 1:
            if destField2.is_empty == False and destField2.color != currColor and destField2.number_of_checkers > 1:
                return False

        return True
        
                 
    @property
    def currDice(self):
        return self._currNum

    @property
    def isRandomized(self):
        return self._isRandomized

    @property
    def isDiceChosen(self):
        return self._isDiceChosen

    @isDiceChosen.setter
    def isDiceChosen(self, new_amount):
        self._isDiceChosen = new_amount

    @isRandomized.setter
    def isRandomized(self, new_amount):
        self._isRandomized = new_amount