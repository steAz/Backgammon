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
        if is_empty == True:
            'empty field'
            
        
        