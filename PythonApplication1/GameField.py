'''
Created on 18 maj 2017

@author: Oskar/Kazan
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
            self._number_of_checkers = number_of_checkers
            self._color = color
            self._is_empty = is_empty
        else :
            self._number_of_checkers = 0
            self._is_empty = is_empty
            self._color = color
    
    @property
    def number_of_checkers(self):
        return self._number_of_checkers
    
    @property
    def is_empty(self):
        return self._is_empty
    
    @property
    def color(self):
        return self._color
    
    @number_of_checkers.setter
    def number_of_checkers(self, new_amount=0):
        self._number_of_checkers = new_amount
    
    @color.setter
    def color(self, new_color=Color.RED):
        self._color = new_color
    
    @is_empty.setter
    def is_empty(self, new_state = True):
        self._is_empty = new_state
    
            
            
        
        