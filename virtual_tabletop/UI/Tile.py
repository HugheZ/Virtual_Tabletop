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
        if game is not None:
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
            if img is not None and img != '':
                pm = QtGui.QPixmap()
                pm.loadFromData(img)
                self.gameImage.setPixmap(pm)
            else:
                self.gameImage.setPixmap(QtGui.QPixmap(":/icons/not-found.png"))
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
            raise Exception('Tiles only support loading {0} or {1} data, not {2}'.format(Game, GameCollection, type(game)))
    
    def setOnline(self, online:bool):
        '''Sets whether this game is online or not\n
        online: True for online, False for not online
        '''
        self.cloudAvailable.setEnabled(online)
        self.upload_action.setEnabled(not online)

    def setLocal(self, local:bool):
        '''Sets whether this game is local or not\n
        local: True for local, False for not local
        '''
        self.localAvailable.setEnabled(local)
        self.download_action.setEnabled(not local)

    @QtCore.pyqtSlot()
    def __game_on_click(self):
        '''Handler for button slot that sends the information up
        '''
        self.loadSignal.emit(self.gameName.text())
    
    # def paintEvent(self, ev):
    #     paint = QtGui.QPainter(self)
    #     shadow = QtGui.QPainter(self)
    #     shadow.begin(self)
    #     paint.begin(self)
    #     #grad = QtGui.QLinearGradient(QtCore.QRectF(self.rect()).bottomLeft(), QtCore.QRectF(self.rect()).topRight())
    #     #grad.setColorAt(0.0, QtCore.Qt.black)
    #     #grad.setColorAt(.2, QtCore.Qt.gray)
    #     #shadow.setBrush(grad)
    #     paint.drawRoundedRect(self.rect() - QtCore.QMargins(1, 1, 1, 1), 15.0, 15.0)
    #     shadow.drawLine(self.rect().bottomRight() - QtCore.QPoint(20, 0), self.rect().bottomLeft() + QtCore.QPoint(20, 0))
    #     paint.end()
    #     shadow.end()