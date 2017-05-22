from tkinter import *
from model.GameField import GameField
from logic.Game import *
from model.GameField import Color
from model.BoardState import BoardState
import sys
#import Tkinter

class GameWindow(Frame):
    '''
    class which represents main window in application
    '''

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.game = Game()
        self.master.title("Backgammon Game")
        self.master.geometry("1400x900")
        self.master.resizable(width=False, height=False)
        'setting background image'
        self.__background_image = PhotoImage(file="background.gif")
        self.__red_checker_image = PhotoImage(file="checker_red.gif")
        self.__black_checker_image = PhotoImage(file="checker_black.gif")
        self.__background_label = Label(image=self.__background_image)
        #self.displayField(game_field = GameField(is_empty=False, number_of_checkers=4, color=Color.BLACK), field_number=23)
        #self.displayField(game_field = GameField(is_empty=False, number_of_checkers=1, color=Color.BLACK), field_number=1)
        starting_board = BoardState()
        self.board = starting_board
        self.displayBoardState(board_state=starting_board)
        ''' applcation's main loop '''
        master.bind("<space>",self.game.setRandNumbers)
        master.bind("<Key-1>", lambda event: self.game.setDice(1, event))
        master.bind("<Key-2>", lambda event: self.game.setDice(2, event))
        master.bind('<Escape>', self.close)
        self.mainloop()

    def close(self, event):
        self.master.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing

    def displayBoardState(self, board_state=None):
        self.place_forget()
        self.__background_label.place(x=0, y=0, relwidth=1, relheight=1)
        if board_state != None:
            fields = board_state._BoardState__fields_states
            index=0
            for field in fields:
                self.displayField(field, index)
                index+=1
        
    def displayField(self, game_field, field_number):
        if game_field.is_empty == False:
            if game_field.color == Color.RED:
               img = self.__red_checker_image
            else:
               img=self.__black_checker_image
            
            x_coord=700
            y_coord=400
                
            number_label = Label(text=str(game_field.number_of_checkers))
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
            Button(image=img, command=lambda no=field_number: self.buttonPressed(no)).place(x=x_coord, y=y_coord)
    
    def buttonPressed(self, fieldNum=0):
        if self.game.isRandomized == True and self.game.isDiceChosen == True:
            #number = self.board._BoardState__fields_states[fieldNumber].number_of_checkers
            #self.board._BoardState__fields_states[fieldNumber].number_of_checkers = number + 1
            #self.displayBoardState(self.board)
            'changing boards state'
            self.game.makeTurn(self.board, fieldNum)
            self.game.isRandomized = False
            self.displayBoardState(self.board)
            
        
        
        #display_label.grid()
        