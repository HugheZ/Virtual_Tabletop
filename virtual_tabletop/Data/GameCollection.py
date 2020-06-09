class GameCollection():
    '''
    A collection of games stored in Firebase as a collection and locally as a folder. It does not hold information about each game but rather about logical storage. When opened, the collection in Firebase will be pinged for metadata, and then once loaded, Games will be filled by locality. Once loaded, refresh will only occur when an update is given by the Firebase API.
    '''

    def __init__(self, name=None, path='/', games=None):
        '''
        Constructor, sets a GameCollection with a given name and pings Firebase for its game data, comparing against local copies.\n
        name: the name of this GameCollection\n
        path: the path in Firebase and locally in localboards\n
        games: the collection of Games generated from Firebase and local storage
        '''
        pass