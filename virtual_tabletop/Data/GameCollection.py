from .Game import Game

class GameCollection():
    '''
    A collection of games stored in Firebase as a collection and locally as a folder. It does not hold information about each game but rather about logical storage. When opened, the collection in Firebase will be pinged for metadata, and then once loaded, Games will be filled by locality. Once loaded, refresh will only occur when an update is given by the Firebase API.
    '''

    def __init__(self, name=None, games=[]):
        '''
        Constructor, sets a GameCollection with a given name and pings Firebase for its game data, comparing against local copies.\n
        name: the name of this GameCollection\n
        games: the collection of Games generated from Firebase and local storage
        '''
        self.name = name
        self.games = []

        for game in games:
            self.addGame(game)
    
    def addGame(self, game):
        if type(game) == Game:
                self.games.append(game)
        elif type(game) == GameCollection:
            self.games.append(GameCollection)
        elif type(game) == dict:
            if game['type'] == 'game':
                self.games.append(Game(game.get('name'),
                    game.get('width'),
                    game.get('height'),
                    game.get('preview_image'),
                    game.get('board')))
            elif game['type'] == 'collection':
                self.games.append(GameCollection(game.get('name'),
                    game.get('games')))
            else:
                raise TypeError("Invalid game for game collection:\nExpected Game or GameCollection JSON, but the one provided could not be parsed. Perhaps it is malformatted.")
        else:
            raise TypeError("Invalid game for game collection:\nExpected {0} or {1} but received {2}".format(Game, GameCollection, type(game)))