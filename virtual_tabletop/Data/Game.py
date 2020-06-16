class Game():
    '''
    A data class to hold information about a given virtualized game.
    '''

    def __init__(self, name=None, width=0, height=0, preview_image=None, board=None, local=None):
        '''
        Constructor, sets the game data by given constructor args. If name is specified, it will check the base directory for locality.\n
        name: game name\n
        width: width to render the board\n
        height: height to render the board\n
        preview_image: the image URL/path shown as a preview on the UI, blank if not provided\n
        board: the actual board image URL/path\n
        local: boolean whether the board is local or not
        '''
        self.name = name
        self.preview_image = preview_image
        self.width = width
        self.height = height
        self.board = board
        self.local = local

        #actual board image, hidden for abstraction
        self.__board = None
        #actual preview image, hidden for abstraction
        self.__preview = None

        #TODO: load board if local
    
    def loadImage(self):
        pass

    def getImage(self):
        pass

        