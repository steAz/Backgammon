from abc import ABCMeta

class Participant:
    __metaclass__ = abc.ABCMeta

    @abstractMethod
    def makeMove(self):
        pass
