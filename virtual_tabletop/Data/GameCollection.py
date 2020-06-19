from .Game import Game
import pyrebase
from collections import OrderedDict

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

        if type(games) == dict or type(games) == OrderedDict:
            games = games.items()

        for game in games:
            self.addGame(game)
    
    def addGame(self, game):
        if type(game) == Game:
                self.games.append(game)
        elif type(game) == GameCollection:
            self.games.append(GameCollection)
        elif type(game) == tuple:
            if game[1]['type'] == 'game':
                self.games.append(Game(game[0],
                    game[1].get('width'),
                    game[1].get('height'),
                    game[1].get('preview_image'),
                    game[1].get('board')))
            elif game[1]['type'] == 'collection':
                self.games.append(GameCollection(game[0],
                    game[1].get('games')))
            else:
                raise TypeError("Invalid game for game collection:\nExpected Game or GameCollection JSON, but the one provided could not be parsed. Perhaps it is malformatted.")
        else:
            raise TypeError("Invalid game for game collection:\nExpected {0} or {1} but received {2}".format(Game, GameCollection, type(game)))
    
    def __len__(self):
        '''Simple length function, returns length of games list'''
        return len(self.games)
    
    def __iter__(self):
        '''Simple iterator function, returns the games list's iterator'''
        return iter(self.games)
    
    def __str__(self):
        '''Returns a string representation of this game collection object:\n
        Name:
        [
            game
            game
            game
        ]
        '''
        ret = self.name + ':\n[\n'
        for game in self.games:
            ret += str(game) + '\n'
        
        return ret + ']'