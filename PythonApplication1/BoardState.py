'''
Created on 21 maj 2017

@author: Oskar/Kazan
'''

from GameField import GameField
from GameField import Color

class BoardState:
    '''
    class which represents state of board at the moment.
    '''


    def __init__(self, fields = None):
        self._fields_states = []
        self._redsOnBand = 0
        self._blacksOnBand = 0
        self._blacksOnTheCourt = 0
        self._redsOnTheCourt = 0
        if fields == None:
            self._fields_states = BoardState.startingBoardState()
        else:
            self._fields_states = fields
            
    
    @staticmethod
    def startingBoardState():
        'static method which returns list of 24 fields containing starting state'
        default_fields = []
        #default_fields.append(GameField(False, 2, Color.BLACK)) #5
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))   
        #default_fields.append(GameField(is_empty=True))                                                                    
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(False, 5, Color.RED))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(False, 3, Color.RED))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(False, 5, Color.BLACK)) #3
        #default_fields.append(GameField(False, 5, Color.RED))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(False, 3, Color.BLACK)) #5
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(False, 5, Color.BLACK)) #5
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(is_empty=True))
        #default_fields.append(GameField(False, 2, Color.RED))

        default_fields.append(GameField(is_empty=True)) #5
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))   
        default_fields.append(GameField(is_empty=True))                                                                    
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True)) #3
        default_fields.append(GameField(False, 15, Color.RED))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True)) #5
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(is_empty=True)) #5
        default_fields.append(GameField(is_empty=True))
        default_fields.append(GameField(False, 2, Color.BLACK))
        default_fields.append(GameField(False, 3, Color.BLACK))
        default_fields.append(GameField(False, 8, Color.BLACK))
        default_fields.append(GameField(False, 2, Color.BLACK))
        
        return default_fields
                              
        
        
        #def update_field_at_index(self, index, game_field):
        #    fields_states.insert(index, game_field) 

        #@property
        #def fields_states(self):
        #    return self.__fields_states
                              
                              
                              
                              
                              
                                 