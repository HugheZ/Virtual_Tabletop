class Game():
    '''
    A data class to hold information about a given virtualized game.
    '''

    def __init__(self, name=None, preview_image=None, board=None, local=None):
        '''
        Constructor, sets the game data by given constructor args. If name is specified, it will check the base directory for locality.\n
        name: game name\n
        preview_image: the image shown as a preview on the UI, blank if not provided\n
        board: the actual board image, shown as png/jpeg\n
        local: boolean whether the board is local or not. If not, board will be None
        '''
        pass

        