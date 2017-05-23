'''
Created on 17 maj 2017

@author: Oskar/Kazan
'''

from tkinter import *
from view.GameWindow import GameWindow


def main():
    root = Tk()
    app = GameWindow(master=root)

if __name__ == '__main__':
    main()