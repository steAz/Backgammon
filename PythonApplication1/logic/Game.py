from tkinter import *
from random import randint
from model.GameField import *


class Game:
    @property
    def player(self):
        return self.__player

    def __init__(self, board):
        self.__isRandomized = False
        self.__isDiceChosen = False
        self.__labelDiceI = None
        self.__labelDiceII = None
        self.__currNumI = None
        self.__currNumII = None
        self.__currNum = None
        self.__amountOfMoves = None
        self.__board = board

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


    def makeTurn(self, fieldNum, currentColor):  # return True means that move has passed
        isNormalValidation = True
        if self.isEverythingAtHome(currentColor) == True:
            print("isEverythingAtHome")
            isNormalValidation = False

        if isNormalValidation == True:
            if self.isValidMove(fieldNum, currentColor) == False:
                print("isValidMove")
                return False
            return self.normalMove(fieldNum, currentColor)
        else: 
            return self.homeMove(fieldNum, currentColor)

    
    def homeIndexes(self, color):
        if color == Color.RED:
            return range(6)
        else:
            return range(18,24)
          

    def isAnotherFieldsToTheCourt(self, fieldNum, playerColor, isLastMove=True):
        if isLastMove == True:
            secondDice = self.__currNum
        elif self.__currNum == self.__currNumI:
            secondDice = self.__currNumII
        else:
            secondDice = self.__currNumI
            
        for i in self.homeIndexes(playerColor):
            if i != fieldNum:
                if self.fieldsToTheCourt(playerColor, i) == self.__currNum or self.fieldsToTheCourt(playerColor, i) == secondDice:
                    field = self.__board._BoardState__fields_states[i]
                    if field.is_empty == False and field.color == playerColor:
                        return True
        return False

    def isAnotherFurther(self, fieldNum, playerColor):
        for i in self.homeIndexes(playerColor):
            if i != fieldNum:
                if self.fieldsToTheCourt(playerColor, i) > self.fieldsToTheCourt(playerColor, fieldNum):
                   # print("I")
                    if self.isFieldInTheSameColor(i, playerColor) == True:
                        #print("numer:  " + str(i)  + str(self.__board._BoardState__fields_states[i].is_empty))
                        return True
        return False

    def isFieldInTheSameColor(self, fieldNum, playerColor):
        field = self.__board._BoardState__fields_states[fieldNum]
        if field.is_empty == False and field.color == playerColor:
            return True
        else:
            return False

    def homeMove(self, fieldNum, playerColor):
        if playerColor == Color.RED:
            destNumber = fieldNum - self.__currNum
        else:
            destNumber = fieldNum + self.__currNum
        destField = self.__board._BoardState__fields_states[destNumber]

        if self.__amountOfMoves == 1: #jesli jest to ostatni ruch
            if self.fieldsToTheCourt(playerColor, fieldNum) == self.__currNum:   #jesli nasza pozycja jest na pozycji wybranej kostki, to wyjdz na dwor
                self.moveToTheCourt(fieldNum, playerColor)
                return True
            elif self.isAnotherFieldsToTheCourt(fieldNum, playerColor) == True:
                print("isAnotherFieldsToTheCourt")
                return False
            elif self.isAnotherFurther(fieldNum, playerColor) == True: 
                print("isAnotherFurther")
                return False
            elif destNumber <= 23 and destNumber >= 0:
                field = self.__board._BoardState__fields_states[fieldNum]
                return self.moveCheckerStandard(destField, field, playerColor) # make normal move
            else:
                self.moveToTheCourt(fieldNum, playerColor)
                return True
        else: # jesli zostal jeszcze jeden ruch, albo wiecej przy dublecie
            if self.fieldsToTheCourt(playerColor, fieldNum) == self.__currNumI or self.fieldsToTheCourt(playerColor, fieldNum) == self.__currNumII:
                #chosen field is correct (distance to court equals dice's roll)
                if self.fieldsToTheCourt(playerColor, fieldNum) == self.__currNum:
                    self.moveToTheCourt(fieldNum, playerColor)
                    return True
                elif destNumber <= 23 and destNumber >= 0:
                    field = self.__board._BoardState__fields_states[fieldNum]
                    return self.moveCheckerStandard(destField, field, playerColor) # make normal move
                else:
                    self.moveToTheCourt(fieldNum, playerColor)
                    return True
            else:
                if self.isAnotherFieldsToTheCourt(fieldNum, playerColor, False) == True: # szukamy czy inne pole jest rowne ktorejs z 2 kostek
                    print("isAnotherFieldsToTheCourt_2")
                    return False
                elif self.isAnotherFurther(fieldNum, playerColor) == True:
                    print("isAnotherFurther_2")
                    return False
                elif destNumber <= 23 and destNumber >= 0:
                    field = self.__board._BoardState__fields_states[fieldNum]
                    return self.moveCheckerStandard(destField, field, playerColor) # make normal move
                else:
                    self.moveToTheCourt(fieldNum, playerColor)
                    return True


    def fieldsToTheCourt(self, currColor, fieldNum):
        if currColor == Color.RED:
            return fieldNum + 1
        else:
            return 24 - fieldNum 

    def moveToTheCourt(self, fieldNum, playerColor):
        print("movetoTheCOurt called")
        if playerColor == Color.RED:
            self.__board._BoardState__redsOnTheCourt += 1
        else:
            self.__board._BoardState__blacksOnTheCourt += 1

        field =  self.__board._BoardState__fields_states[fieldNum]
        field.number_of_checkers -= 1
        if field.number_of_checkers == 0:
            field.is_empty = True 
        
    # method returns true if we can move checker from fieldNumber by self.__currNum positions ## IT DOESTN CHECK THE HOME VALIDATION WHEN PLAYER WANTS TO WIN ##
    def isValidMove(self, fieldNumber, playerColor):
        if playerColor == Color.RED:
            destNumber = fieldNumber - self.__currNum
        else:
            destNumber = fieldNumber + self.__currNum

        if destNumber > 23 or destNumber < 0:
            return False
        destField = self.__board._BoardState__fields_states[destNumber]

        if destField.color != playerColor and destField.number_of_checkers > 1:
            return False
        
        return True

        
    def normalMove(self, fieldNum, currentColor):
        if currentColor == Color.RED:
            destNumber = fieldNum - self.__currNum
            isRed = True
        else:
            destNumber = fieldNum + self.__currNum
            isBlack = False

        destField = self.__board._BoardState__fields_states[destNumber]
        currField = self.__board._BoardState__fields_states[fieldNum]
        return self.moveCheckerStandard(destField, currField, currentColor) # make normal move


    def moveCheckerStandard(self, destField, currField, currColor):   
        if destField.is_empty == True:
            self.moveToEmpty(destField, currField)
            return True
        if destField.color == currField.color:
            self.moveToOur(destField, currField)
            return True
        elif destField.color != currColor and destField.number_of_checkers == 1:
            self.hitEnemy(destField, currField)
            return True
        else:
            print("move checker standard")
            return False

        
    def isEverythingAtHome(self, currentColor):
        amountOfCheckersAtHome = 0
        if currentColor == Color.RED:
            for i in range(18):
                if self.__board._BoardState__fields_states[i + 6].color == currentColor and self.__board._BoardState__fields_states[i + 6].is_empty == False:
                    return False    #amountOfCheckersOutOfHome += self.__board._BoardState__fields_states[i + 5].number_of_checkers
            if self.__board._BoardState__redsOnBand > 0:
                return False
            else:
                return True
        else:
            for i in range(18):
                if self.__board._BoardState__fields_states[i].color == currentColor and self.__board._BoardState__fields_states[i].is_empty == False:
                    return False    #amountOfCheckersOutOfHome += self.__board._BoardState__fields_states[i + 5].number_of_checkers
            if self.__board._BoardState__blacksOnBand > 0:
                return False
            else:
                return True


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

    def moveToEmptyFromBand(self, destField, currColor):
        destField.is_empty = False
        destField.number_of_checkers = 1
        destField.color = currColor
        if currColor == Color.RED:
            self.__board._BoardState__redsOnBand -= 1
        else:
            self.__board._BoardState__blacksOnBand -=1
            

    def moveToOur(self, destField, currField):
        destField.number_of_checkers += 1
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True


    def moveToOurFromBand(self, destField, currColor):
        destField.number_of_checkers += 1
        if currColor == Color.RED:
            self.__board._BoardState__redsOnBand -= 1
        else:
            self.__board._BoardState__blacksOnBand -=1


    def hitEnemy(self, destField, currField):
        currField.number_of_checkers -= 1
        destField.color = currField.color
        if destField.color == Color.BLACK:
            self.__board._BoardState__redsOnBand += 1
        else:
            self.__board._BoardState__blacksOnBand += 1

        if currField.number_of_checkers == 0:
            currField.is_empty = True

    def hitEnemyFromBand(self, destField, currColor):
        destField.number_of_checkers = 1
        destField.color = currColor
        if currColor == Color.RED:
            self.__board._BoardState__redsOnBand -= 1
            self.__board._BoardState__blacksOnBand += 1
        else:
            self.__board._BoardState__blacksOnBand -=1
            self.__board._BoardState__redsOnBand += 1

    def removeFromBand(self, currColor):
        if currColor == Color.RED:
            destField = self.__board._BoardState__fields_states[24 - self.__currNum]
        else:
            destField = self.__board._BoardState__fields_states[self.__currNum - 1]

        if destField.is_empty == True:
            print("empty")
            self.moveToEmptyFromBand(destField, currColor)
        elif destField.color == currColor:
            print("our")
            self.moveToOurFromBand(destField, currColor)
        elif destField.number_of_checkers == 1:
            self.hitEnemyFromBand(destField, currColor)
        else:
            # there are more than 1 enemy checker on the destination field
            pass
        
                 
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