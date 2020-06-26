from virtual_tabletop.Data.Game import Game
import pyrebase
from collections import OrderedDict
from typing import Union

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
                print(game[1])
                self.games.append(Game(game[0],
                    game[1].get('width'),
                    game[1].get('height'),
                    game[1].get('preview_image'),
                    game[1].get('board'),
                    local=False,
                    online=True)) #TODO: defaults to online, still need to check local
            elif game[1]['type'] == 'collection':
                self.games.append(GameCollection(game[0],
                    game[1].get('games')))
            else:
                raise TypeError("Invalid game for game collection:\nExpected Game or GameCollection JSON, but the one provided could not be parsed. Perhaps it is malformatted.")
        else:
            raise TypeError("Invalid game for game collection:\nExpected {0} or {1} but received {2}".format(Game, GameCollection, type(game)))
    
    def find(self, game:Union[str, Game]):
        '''Finds the given game in the game list, returning it or None if not found\n
        game: the game to find
        '''
        try:
            l = lambda g, gother : g == gother
            if type(game) == str:
                l = lambda g, gother : g == gother.name
            for g in self.games:
                print(str(g) + ' == ' + str(game) + ': ' + str(l(game, g)))
            return next(val for x, val in enumerate(self.games) if l(game, val))
        except Exception as e:
            print(str(e))
            return 
    
    def __getitem__(self, key):
        '''Overrides the [] operator'''
        return self.games[key]
    
    def __setitem__(self, key, value):
        '''Overrides the [] = operator'''
        if type(value) not in [Game, GameCollection]:
            raise TypeError('Game Collection only supports adding Games or Game Collections')
        if key < 0 or key > len(self.games):
            raise IndexError('Index given out of bounds of games list')
        self.games[key] = value
    
    def __eq__(self, obj):
        '''Returns true if self and obj are the same collection'''
        return isinstance(obj, GameCollection) and self.name == obj.name and len(self.games) == len(obj.games) and self.games == obj.games

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
    
    def jsonify(self):
        '''Returns a json representation of this game collection for saving purposes'''
        return {
        "type": "collection",
        "name": self.name,
        "games": {game.name : game.jsonify() for game in self.games}
        }
        
