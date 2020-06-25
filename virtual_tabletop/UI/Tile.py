from virtual_tabletop.UI.Tile_UI import Ui_Tile
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore 
from virtual_tabletop.Data.GameCollection import GameCollection
from virtual_tabletop.Data.Game import Game
from typing import Union

class Tile(QtWidgets.QWidget, Ui_Tile):
    '''
    A generic tile UI class to hold information about a shown board.

    The tile will display a preview image of the board, an icon to show whether or not it is stored locally, and a name.

    Collection tiles will alternatively display a folder icon and omit a game image and a 'displayed locally' icon
    '''
    loadSignal = QtCore.pyqtSignal(str)

    def __init__(self, game:Union[Game, GameCollection]=None, *args, **kwargs):
        '''Standard init function for the tile, takes an additional kwarg game for loading games or game collections'''
        super(Tile, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # TODO: AAAA it's 1:20AM and it's dumb that QT auto-sets all children to have a drop shadow!
        # self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(3)
        # self.shadow.setXOffset(-2)
        # self.shadow.setYOffset(-2)
        # self.setGraphicsEffect(self.shadow)

        #load game if given
        if game:
            self.loadGame(game)
        
        print(self.gameName.text())

        #set up signals for pressing buttons
        self.loadButton.clicked.connect(self.__game_on_click)

    
    def loadGame(self, game: Union[Game, GameCollection]):
        '''Loads a user-defined game into this specific tile\n
        game: a game or game collection to be loaded to this tile
        '''
        if type(game) == Game:
            print(game)
            self.gameName.setText(game.name)
            img = game.getPreview()
            if img:
                pm = QtGui.QPixmap()
                pm.loadFromData(img)
                self.gameImage.setPixmap(pm)
            self.localAvailable.setEnabled(game.local)
            self.cloudAvailable.setEnabled(game.online)
        elif type(game) == GameCollection:
            print(game)
            self.gameName.setText(game.name)
            self.gameImage.setPixmap(QtGui.QPixmap(":/icons/collection.png"))
            self.loadButton.setText('Open Collection')
        else:
            raise Exception('Tiles only support loading Game or GameCollection data')
    
    @QtCore.pyqtSlot()
    def __game_on_click(self):
        '''Handler for button slot that sends the information up
        '''
        self.loadSignal.emit(self.gameName.text())