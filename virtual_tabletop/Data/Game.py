import requests

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

        #TODO: load board if local

        #TODO: local board field integration
        self.__board_path = None
        self.__preview_path = None

        #TODO: if local, copy image to local storage
    
    def loadImage(self):
        ret = None
        #use local first
        if self.local:
            with open(self.__board_path) as f:
                ret = f.read()
        else:
            ret = requests.get(self.board).content
        self.__board = ret

    def getImage(self):
        if self.__board is None:
            self.loadImage()
        return self.__board

    def getPreview(self):
        '''Returns the string preview image
        '''
        if self.local:
            if self.__preview_path is None:
                return None
            return open(self.__preview_path)
        else:
            if self.preview_image is None:
                return None
            return requests.get(self.preview_image).content
    
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

        