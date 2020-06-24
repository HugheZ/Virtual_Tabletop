from virtual_tabletop.UI.MainWindow_UI import Ui_VTTMainWindow
from virtual_tabletop.UI.Tile import Tile
from virtual_tabletop.UI.Settings import Settings
from PyQt5 import QtWidgets, QtCore
from virtual_tabletop.Data.GameCollection import GameCollection
from virtual_tabletop.Data.Game import Game
from typing import Optional, Union
from virtual_tabletop.Connections.FirebaseConnector import Connector
from os import path
import json

class MainWindow(QtWidgets.QMainWindow, Ui_VTTMainWindow):
    '''A simple wrapper class for the auto-generated MainWindow_UI-defined main window class'''

    def __init__(self, source: Optional[Connector] = None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #game data pulled from DB
        self.data = None
        #source info
        self.source = None
        #open games
        self.openGames = []

        #connect data source if applicable
        if source:
            try:
                self.connectToSource(source)
            except Exception as e:
                self.showError(e)
        
        #Connect slots and signals
        self.actionSet_Firebase.triggered.connect(self.__rebase)
        self.actionLog_in_preferences.triggered.connect(self.__launch_config_dialog)
    
    def connectToSource(self, source: Connector):
        '''Connects this window to a data source\n
        source: the source to connect to
        '''
        self.source = source
        self.source.watch(self, self.__updateData)
    
    def rebaseSource(self, newKey: str):
        '''Rebases the tracked DB to follow the new key path after saving the new path to the config file\n
        newKey: the path to the new key to track
        NOTE: if the key given does not exist, no changes are made to the source
        '''
        if not path.exists(newKey):
            raise FileNotFoundError('No firebase key file found at given directory')
        #update config file
        config = None
        with open('config.json') as f:
            config = json.load(f)
        config['key_path'] = newKey
        with open('config.json', 'w') as f:
            json.dump(config, f)
        #rebase source
        del self.source
        savedir = config.get('savedir')
        if not savedir:
            savedir = path.join('.','localboards')
        source = Connector(key=newKey, email=config.get('email'), password=config.get('password'), savedir=savedir)
        self.connectToSource(source)

        #reset navigation
        self.toggleBack(False)
        #TODO: close all open boards
    
    def __updateData(self, data: GameCollection):
        '''Handle for updating local data and setting off UI update\n
        data: the data pulled from DB to replace old data with
        '''
        self.data = data
        self.loadLevel(data, self.source.getLocation())

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
            t.loadSignal.connect(self.__game_selected)
            litem.setSizeHint(t.maximumSize())
            self.gamesList.addItem(litem)
            self.gamesList.setItemWidget(litem, t)
        
        #set breadcrumbs
        self.breadcrumbs.setText('> ' + level)
    
    def loadGame(self, game: Game):
        '''Loads the specified game to the open games\n
        game: the Game to load
        '''
        self.openGames.append(game)
        #TODO: load on other screen

    def toggleBack(self, toggle: Optional[bool] = None):
        '''Toggles whether or not the back button is enabled\n
        toggle: whether to enable/disable the back button, default will flip the current state
        '''
        back = toggle if toggle else not self.backButton.isEnabled()
        self.backButton.setEnabled(back)
    
    ###########################################################
    ##                         SLOTS                         ##
    ###########################################################

    @QtCore.pyqtSlot(str)
    def __game_selected(self, gameSelected: str):
        '''Slot defined to parrot signal from selected tile to the DB controller\n
        gameSelected: the game / game collection selected by the user
        '''
        game = self.data.find(gameSelected)
        #if collection, go down to that collection
        if type(game) == GameCollection:
            self.source.goDown(game.name)
            self.toggleBack(True)
        elif type(game) == Game: #else load that game
            self.loadGame(game)
        else: raise Exception('Game selected was neither game or game collection')
    
    @QtCore.pyqtSlot()
    def __return_in_hierarchy(self):
        '''Returns in the hierarchy, setting the up button to disabled if at root
        '''
        self.source.goUp()
        if self.source.getLocation() == '':
            self.toggleBack(False)
    
    @QtCore.pyqtSlot()
    def __rebase(self):
        '''Slot defined to open file browser and select new path to pull firebase data from.\n
        On new key selection, a new Connector object will be linked.
        '''
        key = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select Firebase key', filter='JSON (*.json)')[0]

        #if key is null, there is no new selection, so return
        if key == '':
            return
        
        #rebase
        self.rebaseSource(key)
    
    @QtCore.pyqtSlot()
    def __launch_config_dialog(self):
        '''Launches the config dialog to change user settings
        '''
        config = None
        with open('config.json') as f:
            config = json.load(f)
        dlg = Settings(parent=self, config=config)
        dlg.exec_()
        print(config)
        #modality stopped, save config
        with open('config.json', 'w') as f:
            json.dump(config, f)

    
    #TODO: slots for logging in / out, making new game / game collection
    


    #############################################################
    ##                         DIALOGS                         ##
    #############################################################

    def showError(self, message):
        '''Opens a message to the user that an error occured
        '''
        err = QtWidgets.QMessageBox()
        err.setIcon(QtWidgets.QMessageBox.Critical)
        err.setText('An error has occured when completing this action.')
        err.setInformativeText('Select more info for more.')
        err.setWindowTitle('Error')
        err.setDetailedText(str(message))
        err.setStandardButtons(QtWidgets.QMessageBox.Ok)
        err.exec_()
    
    def openCredentialsDialog(self):
        '''Opens a credentials dialog that asks for user sign-in info
        '''
        #TODO
        return {}
