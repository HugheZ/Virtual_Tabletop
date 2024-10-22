from virtual_tabletop.UI.MainWindow_UI import Ui_VTTMainWindow
from virtual_tabletop.UI.Tile import Tile
from virtual_tabletop.UI.Settings import Settings
from virtual_tabletop.UI.Login import LoginDialog
from virtual_tabletop.UI.OpenGame import OpenGame
from virtual_tabletop.UI.NewGame import NewGame
from virtual_tabletop.UI.BoardWindow import BoardWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from virtual_tabletop.Data.GameCollection import GameCollection
from virtual_tabletop.Data.Game import Game
from typing import Optional, Union
from virtual_tabletop.Connections.FirebaseConnector import Connector
from os import path
import json
from functools import partial

class MainWindow(QtWidgets.QMainWindow, Ui_VTTMainWindow):
    '''A simple wrapper class for the auto-generated MainWindow_UI-defined main window class'''

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #game data pulled from DB
        self.data = None
        #source info
        self.source = None
        #open games local list, separate from openGames widget
        self.openGamesList = []

        #connect data source
        config = None
        source = None
        with open('config.json') as f:
            config = json.load(f)
        #get credentials if we need to
        creds = {'email': None, 'password': None}
        if config.get('login_on_startup'):
            creds = self.getCredentials()
        source = Connector(key=config.get('key_path'), savedir=config['savedir'])
        try:
            source.login(creds['email'], creds['password'])
        except Exception as e:
            self.showError(e)
        try:
            self.connectToSource(source, True)
        except Exception as e:
            self.showError(e)
        #set up login/out toggle
        self.tryToggleLogin(False)

        #open secondary window if coords are given
        #if secondaryWindowCoord is not None:
        secondaryScreen = QtWidgets.QMainWindow(parent=self, flags=QtCore.Qt.Window)
        self.secondaryScreen = secondaryScreen
        self.gamesArea = QtWidgets.QMdiArea(parent=self.secondaryScreen)
        secondaryScreen.setCentralWidget(self.gamesArea)
        desktop = QtGui.QGuiApplication.screens()
        self.secondMonitor = desktop[1].geometry()
        secondaryScreen.move(self.secondMonitor.x(), self.secondMonitor.y())
        secondaryScreen.showFullScreen()
        
        #Connect slots and signals
        self.actionSet_Firebase.triggered.connect(self.__rebase)
        self.actionLog_in_preferences.triggered.connect(self.__launch_config_dialog)
        self.backButton.clicked.connect(self.__return_in_hierarchy)
        self.actionLog_out.triggered.connect(self.__log_out_confirm)
        self.actionLogin.triggered.connect(self.__credentials_launch)
        self.actionGame.triggered.connect(self.__create_game)
        self.actionGame_Collection.triggered.connect(self.__create_game_collection)
        self.actionQuit.triggered.connect(self.close)
    
    def connectToSource(self, source: Connector, echo:bool = False):
        '''Connects this window to a data source\n
        source: the source to connect to\n
        echo: whether to echo error details
        '''
        self.source = source
        self.source.watch(self, self.__updateData)
        self.source.refresh(echo)
    
    def getCredentials(self):
        '''Queries the user for credentials or reads them from file if specified by user that they should be stoed.
        '''
        #parses login preferences to see if we need to also log in
        #If config says to sign in first, do so
        creds = None
        config = None
        with open('config.json') as f:
            config = json.load(f)
        #if we have stored credentials, use them
        if config['storecreds']:
            with open('credentials.json') as c:
                creds = json.load(c)
            if creds.get('password') is None or creds.get('email') is None:
                #no stored credentials, so sign in like normal
                creds = self.openCredentialsDialog()
        else: #else just sign in
            creds = self.openCredentialsDialog()
        return creds if creds is not None else {'email': None, 'password': None}
    
    def login(self, email:str, password:str):
        '''Logs in to the connected source if one exists, else shows error\n
        NOTE: this function also serializes credentials if chosen, need to update on better storage solution
        email: the email used to log in to firebase\n
        password: the password used to log in to firebase
        '''
        try:
            self.source.login(email, password)
            self.source.refresh()
            self.tryToggleLogin(False)
            #see if we need to save the credentials
            config = None
            with open('config.json') as f:
                config = json.load(f)
            if config.get('storecreds', False):
                with open('credentials.json', 'w') as w:
                    json.dump({"email":email, "password":password}, w, indent=3)
        except Exception as e:
            #on login error, get local info and re-enable login button
            self.showError(e)
            self.source.refresh()
            self.tryToggleLogin(True)
    
    def logout(self):
        '''Logs out of the connected source if already logged in, else does nothing
        '''
        self.source.logout()
        self.tryToggleLogin(True)
    
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
            json.dump(config, f, indent=3)
        #rebase source
        del self.source
        #get credentials if needed
        creds = {'email': None, 'password': None}
        if config.get('login_on_startup'):
            creds = self.getCredentials()
        savedir = config.get('savedir')
        if not savedir:
            savedir = path.join('.','localboards')
        source = Connector(key=newKey, savedir=savedir)
        try:
            source.login(creds['email'], creds['password'])
        except Exception as e:
            self.showError(e)
        try:
            self.connectToSource(source)
            #toggle login
            self.tryToggleLogin(True)
        except Exception as e:
            self.showError(e)
            #reset login, didn't work
            self.tryToggleLogin(False)
        #reset navigation
        self.toggleBack(False)
        
        #close all open boards
        self.openGamesList.clear()
        self.openGames.clear()
    
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
        #if no data, return
        if data is None:
            return
        
        #populate list
        for game in data:
            litem = QtWidgets.QListWidgetItem(self.gamesList)
            t = Tile(parent=self.gamesList, game=game)
            t.loadSignal.connect(partial(self.__game_selected, game))
            t.upload_action.triggered.connect(partial(self.__upload, game, t))
            t.download_action.triggered.connect(partial(self.__download, game, t))
            t.delete_action.triggered.connect(partial(self.__delete, game, t))
            litem.setSizeHint(t.maximumSize())
            self.gamesList.addItem(litem)
            self.gamesList.setItemWidget(litem, t)
        
        #set breadcrumbs
        self.breadcrumbs.setText('> ' + level)
    
    def loadGame(self, game: Game):
        '''Loads the specified game to the open games\n
        game: the Game to load
        '''
        #don't add if game is already open
        try:
            ret = next(val for x, val in enumerate(self.openGamesList) if val[0] == game)
            if ret is not None:
                return
        except Exception:
            pass
        #check config, see if we should download the image
        config = {}
        with open('config.json') as f:
            config = json.load(f)
        if config.get('store_on_download') and not game.local:
            #config set to store on download and game is not local, so store it
            #find the tile
            t = None
            def gen():
                for i in range(self.gamesList.count()):
                    widg = self.gamesList.itemWidget(self.gamesList.item(i))
                    if widg.gameName.text() == game.name:
                        yield widg
            t = next(gen())
            self.__download(game, t)
        #initialize subwindow
        label = QtWidgets.QLabel()
        subwin = BoardWindow()
        subwin.setWidget(label)
        #subwin.setWindowTitle(game.name)
        #scale image
        (x,y) = self.__calculateSize(game.width, game.height)
        label.resize(x,y)
        #load movie if game board is gif, else load pixmap
        data = game.getImage()
        if game.isGif():
            movie = QtGui.QMovie(data, b'GIF', label)
            movie.setScaledSize(label.size())
            movie.start()
            label.setMovie(movie)
        else:
            pixm = QtGui.QPixmap()
            pixm.loadFromData(data)
            label.setPixmap(pixm.scaled(label.size()))
        #add to boards
        self.gamesArea.addSubWindow(subwin, QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        #show
        subwin.show()
        #link subwindow with local games list
        toAdd = (game, subwin)
        self.openGamesList.append(toAdd)
        #add to open games list
        litem = QtWidgets.QListWidgetItem(parent=self.openGames)
        customUI = OpenGame(parent=self.openGames)
        litem.setSizeHint(customUI.sizeHint())
        customUI.gameName.setText(game.name)
        self.openGames.addItem(litem)
        self.openGames.setItemWidget(litem, customUI)
        #link closing event
        customUI.closeButton.clicked.connect(partial(self.__closeGame,litem))

    
    def __closeGame(self, caller:QtWidgets.QListWidgetItem):
        '''Closes the signaled game by removing it from the open games list and games subwindow\n
        caller: the listwidgetitem to remove from the list
        '''
        i = self.openGames.row(caller)
        #remove from UI
        item = self.openGames.takeItem(i)
        del item
        #close and remove internal
        win = self.openGamesList[i][1]
        mov = win.findChild(QtGui.QMovie)
        if mov is not None: mov.stop()
        win.close()
        g = self.openGamesList[i][0]
        if g.isGif():
            g.closeStream()
        self.openGamesList.pop(i)
        #REALLY bad code, but we have to search for the qmovie and stop or else we get a seg fault
        #APPARENTLY PyQT, or I guess QT, doesn't stop movies when their parents are deleted when running from a buffer. Dumb.


    def __calculateSize(self, width: Union[int, float], height: Union[int, float]):
        '''Returns a width and height to use for resizing boards\n
        width: width of the board in inches\n
        height: height of the board in inches\n
        '''
        #get x and y DPI (dots / inch)
        xDPI = self.secondaryScreen.physicalDpiX()
        yDPI = self.secondaryScreen.physicalDpiY()
        #get pixel sizes for board
        # pixels = inch * dots/inch
        return (width * xDPI, height * yDPI)

    def toggleBack(self, toggle: Optional[bool] = None):
        '''Toggles whether or not the back button is enabled\n
        toggle: whether to enable/disable the back button, default will flip the current state
        '''
        back = toggle if toggle else not self.backButton.isEnabled()
        self.backButton.setEnabled(back)
    
    def tryToggleLogin(self, enableLogin:bool):
        '''Tries to toggle the log-in action. Checks for if source exists and we aren't logged in\n
        enableLogin: whether we want login (True) to be enabled and logout disabled or vice versa (False)
        '''
        if enableLogin and self.source is not None and not self.source.isLoggedIn():
            self.actionLogin.setEnabled(True)
            self.actionLog_out.setEnabled(False)
        elif not enableLogin and self.source is not None and self.source.isLoggedIn():
            self.actionLogin.setEnabled(False)
            self.actionLog_out.setEnabled(True)
    
    ###########################################################
    ##                         SLOTS                         ##
    ###########################################################

    @QtCore.pyqtSlot(str)
    def __game_selected(self, gameSelected:Union[Game, GameCollection]):
        '''Slot defined to parrot signal from selected tile to the DB controller\n
        gameSelected: the game / game collection selected by the user
        '''
        #if collection, go down to that collection
        if type(gameSelected) == GameCollection:
            self.source.goDown(gameSelected.name)
            self.toggleBack(True)
        elif type(gameSelected) == Game: #else load that game
            self.loadGame(gameSelected)
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
        #modality stopped, save config
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=3)
    
    @QtCore.pyqtSlot()
    def __log_out_confirm(self):
        '''Launches the log-out confirmation modal and logs out if confirmed
        '''
        dlg = QtWidgets.QMessageBox()
        dlg.setIcon(QtWidgets.QMessageBox.Warning)

        dlg.setText("Are you sure you want to log out?")
        dlg.setInformativeText("Non-local games will be lost.")
        dlg.setWindowTitle("Log-out")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if dlg.exec_() == QtWidgets.QMessageBox.Yes:
            self.logout()
    
    @QtCore.pyqtSlot()
    def __credentials_launch(self):
        '''Launches the credentials dialog for logging in
        '''
        creds = self.openCredentialsDialog()

        #if we have creds, try to log in, show error on fail
        if creds is not None:
            self.login(creds['email'], creds['password'])


    @QtCore.pyqtSlot()
    def __create_game(self):
        '''Launches the new game dialog and saves the game local/cloud by config preferences
        '''
        #get the user-given game
        created = self.openNewGameDialog()

        #if game is not none, save
        if created is not None:
            #parse into game
            game = Game(created['name'], created['width'], created['height'], created['preview_image'], created['board'], True, False)
            #create the game locally
            try:
                self.source.addToLocal(game)
                #if config says to auto-upload, do so
                config = None
                with open('config.json', 'r') as f:
                    config = json.load(f)
                if config['auto_upload']:
                    self.source.upload(game)
                #refresh
                self.source.refresh(True)
            except Exception as e:
                self.showError(e)
    
    @QtCore.pyqtSlot()
    def __create_game_collection(self):
        '''Launches dialog for getting new game collection name
        '''
        text, ok = QtWidgets.QInputDialog.getText(self, 'New Collection', 'Input a name for your new Game Collection:')

        #hit ok, should add the collection
        if ok:
            coll = GameCollection(text)
            try:
                self.source.addToLocal(coll)
                #if config says to auto-upload, do so
                config = None
                with open('config.json', 'r') as f:
                    config = json.load(f)
                if config['auto_upload']:
                    self.source.upload(coll)
                #refresh
                self.source.refresh(True)
            except Exception as e:
                self.showError(e)
    
    @QtCore.pyqtSlot()
    def __upload(self, game:Game, tile: Tile):
        '''Uploads the given game selected and sets the appropriate tile to be online\n
        game: the game to upload\n
        tile: the UI Tile to flip availability messages
        '''
        try:
            self.source.upload(game)
            tile.setOnline(True)
        except Exception as e:
            self.showError(e)
    
    @QtCore.pyqtSlot()
    def __download(self, game:Game, tile: Tile):
        '''Downloads the given game selected and sets the appropriate tile to be local\n
        game: the game to download\n
        tile: the UI Tile to flip availability messages
        '''
        try:
            self.source.download(game)
            tile.setLocal(True)
        except Exception as e:
            self.showError(e)
    
    @QtCore.pyqtSlot()
    def __delete(self, game:Game, tile:Tile):
        '''Requests for confirmation of delete request for online, local, or both\n
        game: the game to delete\n
        tile: the UI Tile to flip availability messages
        '''
        items = []
        if game.online: items.append('Online')
        if game.local: items.append('Local')
        if game.online and game.local: items.append('Both')
        item, ok = QtWidgets.QInputDialog.getItem(self, 'Delete game', 'Delete game from...', items)

        if ok and item:
            #deletion request with an item, get proper locality, call delete, refresh, and show any errors
            (local, online) = (True, True) if item == 'Both' else (True, False) if item == 'Local' else (False, True)
            try:
                self.source.delete(game, local, online)
                self.source.refresh(True)
            except AttributeError as e: #if is our attribute error, show the error and refresh
                self.showError(e)
                self.source.refresh(True)
            except Exception as e:
                self.showError(e)
        #else do nothing, no deletion requested





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
        creds = {'email':None,'password':None}
        dlg = LoginDialog(creds=creds, parent=self)

        if dlg.exec_() == QtWidgets.QMessageBox.Ok:
            return creds
        else: return None
    
    def openNewGameDialog(self):
        '''Opens the new game dialog that asks for user-created games
        '''
        #game metadata
        game = {'type':'game', 'name':None, 'width':None, 'height':None, 'board':None, 'preview_image':None}

        #open the dialog
        dlg = NewGame(game=game, parent=self)

        #return only on save
        if dlg.exec_() == QtWidgets.QMessageBox.Save:
            return game
        else: return None
