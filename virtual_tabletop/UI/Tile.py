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

        #set up actions
        self.upload_action = QtWidgets.QAction('Upload', self.changeGameActions)
        self.download_action = QtWidgets.QAction('Download', self.changeGameActions)
        self.delete_action = QtWidgets.QAction('Delete...', self.changeGameActions)
        self.changeGameActions.addAction(self.upload_action)
        self.changeGameActions.addAction(self.download_action)
        self.changeGameActions.addAction(self.delete_action)

        # TODO: AAAA it's 1:20AM and it's dumb that QT auto-sets all children to have a drop shadow!
        # self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(3)
        # self.shadow.setXOffset(-2)
        # self.shadow.setYOffset(-2)
        # self.setGraphicsEffect(self.shadow)

        #load game if given
        if game:
            self.loadGame(game)
        

        #set up signals for pressing buttons
        self.loadButton.clicked.connect(self.__game_on_click)

    
    def loadGame(self, game: Union[Game, GameCollection]):
        '''Loads a user-defined game into this specific tile\n
        game: a game or game collection to be loaded to this tile
        '''
        if type(game) == Game:
            self.gameName.setText(game.name)
            img = game.getPreview()
            if img:
                pm = QtGui.QPixmap()
                pm.loadFromData(img)
                self.gameImage.setPixmap(pm)
            self.localAvailable.setEnabled(game.local)
            self.cloudAvailable.setEnabled(game.online)
            #set actions available depending on location
            if game.local:
                self.download_action.setEnabled(False)
            if game.online:
                self.upload_action.setEnabled(False)
        elif type(game) == GameCollection:
            self.gameName.setText(game.name)
            self.gameImage.setPixmap(QtGui.QPixmap(":/icons/collection.png"))
            self.loadButton.setText('Open Collection')
            #remove menu button if collection
            self.changeGameActions.deleteLater()
        else:
            raise Exception('Tiles only support loading Game or GameCollection data')
    
    @QtCore.pyqtSlot()
    def __game_on_click(self):
        '''Handler for button slot that sends the information up
        '''
        self.loadSignal.emit(self.gameName.text())