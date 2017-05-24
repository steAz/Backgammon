from model.GameField import Color
from logic.Game import Game
from model.BoardState import BoardState

class AImove(object):
   
    def __init__(self, game, color, rollNum, fieldNum):
        self.__fieldNumber = fieldNum
        self.__rollNumber = rollNum
        self.__color = color
        self.__game = game

    def futureMove(self, AIboard):
        if self.__color == Color.RED:
            destNum = self.__fieldNumber - self.__rollNumber
        else:
            destNum = self.__fieldNumber + self.__rollNumber
        currField = AIboard.field_states[self.__fieldNumber]
        destField = AIboard.fields_states[destNum]

        self.moveCheckerStandard(destField, currField, AIboard) # make future move


    def futureMakeTurn(self, AIboard):
        isNormalValidation = True
        if self.isFutureEverythingAtHome(AIboard) == True:
            print("isFutureEverythingAtHome")
            isNormalValidation = False

        if isNormalValidation == True:
            if self.isFutureValidMove(fieldNum, AIboard) == False:
                print("isFutureValidMove")
                return False
            return self.futureMove(AIboard)
        else: 
            return self.futureHomeMove(fieldNum)


    def isFutureValidMove(self, fieldNumber, AIboard):
        if self.__color == Color.RED:
            destNumber = fieldNumber - self.__currNum
        else:
            destNumber = fieldNumber + self.__currNum

        if destNumber > 23 or destNumber < 0:
            return False
        destField = self.__board._BoardState__fields_states[destNumber]

        if destField.color != self.__color and destField.number_of_checkers > 1:
            return False
        
        return True


    def isFutureEverythingAtHome(self, AIboard):
        amountOfCheckersAtHome = 0
        if self.__color == Color.RED:
            for i in range(18):
                if AIboard._BoardState__fields_states[i + 6].color == self.__color and AIboard._BoardState__fields_states[i + 6].is_empty == False:
                    return False    #amountOfCheckersOutOfHome += self.__board._BoardState__fields_states[i + 5].number_of_checkers
            if AIboard._BoardState__redsOnBand > 0:
                return False
            else:
                return True
        else:
            for i in range(18):
                if AIboard._BoardState__fields_states[i].color == self.__color and AIboard._BoardState__fields_states[i].is_empty == False:
                    return False    #amountOfCheckersOutOfHome += self.__board._BoardState__fields_states[i + 5].number_of_checkers
            if AIboard._BoardState__blacksOnBand > 0:
                return False
            else:
                return True


    def moveCheckerStandard(self, destField, currField, AIboard):   
        if destField.is_empty == True:
            self.futureMoveToEmpty(destField, currField)
            return True
        if destField.color == currField.color:
            self.futureMoveToOur(destField, currField)
            return True
        elif destField.color != self.__color and destField.number_of_checkers == 1:
            self.futureHitEnemy(destField, currField, AIboard)
            return True
        else:
            return False

    def futureMoveToEmpty(self, destField, currField):
        destField.is_empty = False
        destField.number_of_checkers = 1
        destField.color = currField.color
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True

    def futureMoveToOur(self, destField, currField):
        destField.number_of_checkers += 1
        currField.number_of_checkers -= 1
        if currField.number_of_checkers == 0:
            currField.is_empty = True


    def futureHitEnemy(self, destField, currField, AIboard):
        currField.number_of_checkers -= 1
        destField.color = currField.color
        if destField.color == Color.BLACK:
            AIboard._BoardState__redsOnBand += 1
        else:
            AIboard._BoardState__blacksOnBand += 1

        if currField.number_of_checkers == 0:
            currField.is_empty = True


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

    def futureHomeMove(self, fieldNum, playerColor):
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


    def boardStateAfterMove(self, AIboard):
        self.futureMove(AIboard)
        return AIboard

        





