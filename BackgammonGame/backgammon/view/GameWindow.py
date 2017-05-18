'''
Created on 17 maj 2017

@author: Oskar
'''

from tkinter import *

class GameWindow(Frame):
    '''
    class which represents main window in application
    '''

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Backgammon Game")
        self.master.geometry("1400x900")
        self.master.resizable(width=False, height=False)
        'setting background image'
        background_image = PhotoImage(file="background.gif")
        background_label = Label(image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        ''' applcation's main loop '''
        mainloop()
        

root = Tk()
app = GameWindow(master=root)