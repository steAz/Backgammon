'''
Created on 18 maj 2017

@author: Oskar
'''
from enum import Enum

'enumeration for colors of checkers'
class Color(Enum):
    RED = 0
    BLACK = 1


class GameField:
    '''
    Class which represents game field. Each field contains some number(or zero) of checkers in 
    one of two colors (black or red)
    '''


    def __init__(self, is_empty=True, number_of_checkers=0, color=Color.RED):
        if is_empty == False:
            self.__number_of_checkers = number_of_checkers
            self.__color = color
            self.__is_empty = is_empty
        else:
            self.__number_of_checkers = 0
            self.__is_empty = is_empty
            self.__color = color
    
    @property
    def number_of_checkers(self):
        return self.__number_of_checkers
    
    @property
    def is_empty(self):
        return self.__is_empty
    
    @property
    def color(self):
        return self.__color
    
    @number_of_checkers.setter
    def number_of_checkers(self, new_amount=0):
        self.__number_of_checkers = new_amount
    
    @color.setter
    def color(self, new_color=Color.RED):
        self.__color = new_color
    
    @is_empty.setter
    def is_empty(self, new_state = True):
        self.__is_empty = new_state
    
            
            
        
        