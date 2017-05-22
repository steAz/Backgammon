
class Game:

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, player):
        self.__player = player