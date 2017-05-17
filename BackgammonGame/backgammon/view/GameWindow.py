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
        ''' applcation's main loop '''
        mainloop()
        

root = Tk()
app = GameWindow(master=root)