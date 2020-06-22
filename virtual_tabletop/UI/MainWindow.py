from virtual_tabletop.UI.MainWindow_UI import Ui_VTTMainWindow
from virtual_tabletop.UI.Tile import Tile
from PyQt5 import QtWidgets, QtCore
from virtual_tabletop.Data.GameCollection import GameCollection
from virtual_tabletop.Data.Game import Game
from typing import Optional

class MainWindow(QtWidgets.QMainWindow, Ui_VTTMainWindow):
    '''A simple wrapper class for the auto-generated MainWindow_UI-defined main window class'''

    #game choice signal
    gameSelected = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #temp add in some game tiles
        # for i in range(6):
        #     litem = QtWidgets.QListWidgetItem(self.gamesList)
        #     t = Tile()
        #     litem.setSizeHint(t.maximumSize())
        #     self.gamesList.addItem(litem)
        #     self.gamesList.setItemWidget(litem, t)
        # self.breadcrumbs.setText('> test')
    

    def loadLevel(self, data: GameCollection, level: str = ''):
        '''Loads a selected level into the main window by the given game collection\n
        data: the collection to load onto the main window\n
        level: the string representation of the current level, defaults to base\n
        '''
        #clear current level
        self.gamesList.clear()
        for game in data:
            litem = QtWidgets.QListWidgetItem(self.gamesList)
            t = Tile(parent=self.gamesList, game=game)
            #t.loadGame(game)
            litem.setSizeHint(t.maximumSize())
            self.gamesList.addItem(litem)
            self.gamesList.setItemWidget(litem, t)
        
        #set breadcrumbs
        self.breadcrumbs.setText('> ' + level)

    def toggleBack(self, toggle: Optional[bool] = None):
        '''Toggles whether or not the back button is enabled\n
        toggle: whether to enable/disable the back button, default will flip the current state
        '''
        back = toggle if toggle else not self.backButton.isEnabled()
        self.backButton.setEnabled(back)
    
    @QtCore.pyqtSlot(str)
    def __game_selected(self, gameSelected):
        '''Slot defined to parrot signal from selected tile to the DB controller
        '''
        print(gameSelected)