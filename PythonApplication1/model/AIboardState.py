from logic.AImove import AImove
from BoardState import BoardState

class AIboardState(BoardState):
    
    def __init__(self, move):
        self.__AImove = move

    def AIbStateAfterMove(self):
        move.makeAImove(self)


