import requests
from PyQt5 import QtCore
from os import path

class Game():
    '''
    A data class to hold information about a given virtualized game.
    '''

    def __init__(self, name=None, width=0, height=0, preview_image=None, board=None, local=False, online=False):
        '''
        Constructor, sets the game data by given constructor args. If name is specified, it will check the base directory for locality.\n
        name: game name\n
        width: width to render the board\n
        height: height to render the board\n
        preview_image: the image URL/path shown as a preview on the UI, blank if not provided\n
        board: the actual board image URL/path\n
        local: boolean whether the board is local or not\n
        online: boolean whetehr the board is online or not
        '''
        self.name = name
        self.preview_image = preview_image
        self.width = width
        self.height = height
        self.board = board
        self.local = local
        self.online = online

        #actual board image, hidden for abstraction
        self.__board = None
        #actual preview image, hidden for abstraction
        self.__preview = None
        #content type, used for gif playing
        self.__isGif = False

        #local board field integration
        self.__board_path = None
        self.__preview_path = None

        #if local, copy image to local storage
        if self.local:
            self.__board_path = board
            self.__preview_path = preview_image
    
    def loadImage(self):
        '''Loads the image, prioritizing local storage. Also refreshes content type.
        '''
        ret = None
        #use local first
        if self.local:
            with open(self.__board_path, 'rb') as f:
                ret = f.read()
            self.__isGif = path.splitext(self.__board_path)[1].lower() == '.gif'
        else:
            resp = requests.get(self.board)
            ret = resp.content
            head = resp.headers.get('content-type')
            self.__isGif = head == 'image/gif'
        if self.__isGif:
            self.array = QtCore.QByteArray(ret)
            self.buff = QtCore.QBuffer(self.array)
            self.buff.open(QtCore.QIODevice.ReadOnly)
            ret = self.buff
        self.__board = ret

    def getImage(self):
        '''Returns the binary data for this game's board image. If the image is instead a gif, returns a binary stream for the data.
        '''
        if self.__board is None:
            self.loadImage()
        return self.__board
    
    def isGif(self):
        '''Returns true if the board to be downloaded is a gif, else false'''
        return self.__isGif
    
    def loadPreview(self):
        '''Loads the preview, prioritizing local storage.
        '''
        ret = None
        if self.local:
            with open(self.__preview_path) as f:
                ret = f.read()
        else:
            ret = requests.get(self.preview_image).content
        self.__preview = ret

    def getPreview(self):
        '''Returns the string preview image
        '''
        if self.__preview is None:
            self.loadPreview()
        return self.__preview
    
    def closeStream(self):
        '''Finalizer to close streams if open'''
        if self.__isGif:
            if not self.array.isEmpty(): self.array.clear()
            if self.buff.isOpen(): self.buff.close()
            del self.array
            del self.buff
            self.__board = None
    
    def __eq__(self, obj):
        '''Returns true if self and obj are the same game
        '''
        return isinstance(obj, Game) and self.name == obj.name and self.height == obj.height and self.width == obj.width and self.board == obj.board and self.preview_image == obj.preview_image

    def __str__(self):
        '''Returns a string representation of this Game object:\n
        name: <width, height> in., local: X, online: X
        '''
        return '{0}: <{1}, {2}> in., local: {3}, online: {4}'.format(
            self.name, self.width, self.height,
            'YES' if self.local else 'NO',
            'YES' if self.online else 'NO' 
        )
    
    def jsonify(self):
        '''Returns a json representation of this game for saving purposes'''
        return {
            "type": "game",
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "board": self.board,
            "preview_image": self.preview_image
        }

        