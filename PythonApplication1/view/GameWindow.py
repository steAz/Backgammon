from tkinter import *
from model.GameField import GameField
from logic.Game import *
from model.GameField import Color
from model.BoardState import BoardState
from logic.AIbot import AIbot
import sys
#import Tkinter

class GameWindow(Frame):
    '''
    class which represents main window in application
    '''

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.__widgets = []
        starting_board = BoardState()
        self.AIbot = AIbot()
        self.board = starting_board
        self.game = Game()
        self.game.__amountOfMoves = 0
        self.master.title("Backgammon Game")
        self.master.geometry("1400x900")
        self.master.resizable(width=False, height=False)
        'setting background image'
        self.__background_image = PhotoImage(file="background.gif")
        self.__red_checker_image = PhotoImage(file="checker_red.gif")
        self.__black_checker_image = PhotoImage(file="checker_black.gif")
        self.__background_label = Label(image=self.__background_image)
        
        self.displayBoardState(starting_board)
        ''' applcation's main loop '''
        master.bind("<space>",self.game.setRandNumbers)
        master.bind("<Key-1>", lambda event: self.game.setDice(1, event))
        master.bind("<Key-2>", lambda event: self.game.setDice(2, event))
        master.bind('<Escape>', self.close)
        self.mainloop()


    def close(self, event):
        self.master.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing

    def displayBandState(self):
        if self.board._BoardState__redsOnBand > 0:
            number_label_red = Label(text=str(self.board._BoardState__redsOnBand))
            self.__widgets.append(number_label_red)
            number_label_red.place(x=693, y=320)
            button_red = Button(image=self.__red_checker_image, command=lambda:self.bandCheckerPressed())
            button_red.place(x=675, y=340)
            self.__widgets.append(button_red)
        if self.board._BoardState__blacksOnBand > 0:
            number_label_black = Label(text=str(self.board._BoardState__blacksOnBand))
            self.__widgets.append(number_label_black)
            number_label_black.place(x=693, y=430)
            button_black = Button(image=self.__black_checker_image)
            button_black.place(x=675, y=450)
            self.__widgets.append(button_black)

    def displayCourtState(self):
           if self.board._BoardState__redsOnTheCourt > 0:
                number_label_red = Label(text=str(self.board._BoardState__redsOnTheCourt))
                self.__widgets.append(number_label_red)
                number_label_red.place(x=1321, y=220)
                button_red = Button(image=self.__red_checker_image)
                button_red.place(x=1303, y=240)
                self.__widgets.append(button_red)
           if self.board._BoardState__blacksOnTheCourt > 0:
                number_label_black = Label(text=str(self.board._BoardState__blacksOnTheCourt))
                self.__widgets.append(number_label_black)
                number_label_black.place(x=1321, y=630)
                button_black = Button(image=self.__black_checker_image)
                button_black.place(x=1303, y=650)
                self.__widgets.append(button_black)



    def displayBoardState(self, board_state=None):
        self.clearLabels()
        self.displayBandState()
        self.displayCourtState()

        self.__background_label.place(x=0, y=0, relwidth=1, relheight=1)
        if board_state != None:
            fields = board_state._BoardState__fields_states
            index=0
            for field in fields:
                self.displayField(field, index)
                index+=1


    def clearLabels(self):
        for label in self.__widgets:
            label.destroy()
        

    def displayField(self, game_field, field_number):
        if game_field.is_empty == False:
            if game_field.color == Color.RED:
               img = self.__red_checker_image
            else:
               img = self.__black_checker_image
  
            number_label = Label(text=str(game_field.number_of_checkers))
            self.__widgets.append(number_label)

            x_coord=700
            y_coord=400
                
            'calculate x and y coordinates'
            if field_number == 0 or field_number == 23:
                x_coord=1186
            elif field_number == 1 or field_number == 22:
                x_coord=1100
            elif field_number == 2 or field_number == 21:
                x_coord=1010
            elif field_number == 3 or field_number == 20:
                x_coord=923
            elif field_number == 4 or field_number == 19:
                x_coord=833
            elif field_number == 5 or field_number == 18:
                x_coord=746
            elif field_number == 6 or field_number == 17:
                x_coord=600
            elif field_number == 7 or field_number == 16:
                x_coord=514
            elif field_number == 8 or field_number == 15:
                x_coord=421
            elif field_number == 7 or field_number == 14:
                x_coord=333
            elif field_number == 10 or field_number == 13:
                x_coord=243
            elif field_number == 11 or field_number == 12:
                x_coord=155
                
            if field_number <= 11:
                y_coord = 100
            else:
                y_coord = 800
            
            number_label.place(x=x_coord + 20, y=y_coord - 20)

            button = Button(image=img, command=lambda no=field_number: self.buttonPressed(no))
            button.place(x=x_coord, y=y_coord)
            self.__widgets.append(button)
    

    def buttonPressed(self, fieldNum=0):
        print(str(self.game._Game__amountOfMoves))
        if self.board._BoardState__fields_states[fieldNum].color == Color.RED: # we can move only red
            if self.game.isRandomized == True and self.game.isDiceChosen == True and self.game._Game__amountOfMoves != 0 and self.board._BoardState__redsOnBand == 0:
                'changing boards state'
                if self.game.makeTurn(self.board,fieldNum, Color.RED) == True:
                    if  self.game._Game__amountOfMoves == 2:
                        if self.game._Game__currNum == self.game._Game__currNumI:
                            self.game.setDice(2)
                        else:
                            self.game.setDice(1)
                    self.game._Game__amountOfMoves -= 1
                    if self.game._Game__amountOfMoves == 0:
                        self.AIbot.makeTurnForBot(self.board)
                        self.game.isRandomized = False
                else:
                    print("niewlasciwy ruch")
                
        self.displayBoardState(self.board)
        
    def bandCheckerPressed(self):
         
         if self.game.isRandomized == True and self.game.isDiceChosen == True and self.game._Game__amountOfMoves != 0:
             self.game.removeFromBand(Color.RED, self.board)
             if  self.game._Game__amountOfMoves == 2:
                 if self.game._Game__currNum == self.game._Game__currNumI:
                    self.game.setDice(2)
                 else:
                    self.game.setDice(1)
             self.game._Game__amountOfMoves -= 1
             if self.game._Game__amountOfMoves == 0:
                self.game.isRandomized = False

             self.displayBoardState(self.board)
            
        
        
        