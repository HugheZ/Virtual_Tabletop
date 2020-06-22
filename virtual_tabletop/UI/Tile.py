from virtual_tabletop.UI.Tile_UI import Ui_Tile
from PyQt5 import QtWidgets, QtGui
from virtual_tabletop.Data.GameCollection import GameCollection
from virtual_tabletop.Data.Game import Game
from typing import Union

class Tile(QtWidgets.QWidget, Ui_Tile):
    '''
    A generic tile UI class to hold information about a shown board.

    The tile will display a preview image of the board, an icon to show whether or not it is stored locally, and a name.

    Collection tiles will alternatively display a folder icon and omit a game image and a 'displayed locally' icon
    '''

    def __init__(self, *args, **kwargs):
        '''Standard init function for the tile, takes an additional kwarg game for loading games or game collections'''
        super(Tile, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #load game if we have one
        if 'game' in kwargs:
            self.loadGame(kwargs['game'])
    
    def loadGame(self, game: Union[Game, GameCollection]):
        '''Loads a user-defined game into this specific tile\n
        game: a game or game collection to be loaded to this tile
        '''
        if type(game) == Game:
            self.gameName = game.name
            self.gameImage = game.getImage()
            self.localAvailable.setEnabled(game.local)
            self.cloudAvailable.setEnabled(game.online)
        elif type(game) == GameCollection:
            self.gameName = game.name
            self.gameImage = QtGui.QPixmap(":/icons/collection.png")
        else:
            raise Exception('Tiles only support loading Game or GameCollection data')