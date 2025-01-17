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

        if games is not None:
            for game in games:
                self.addGame(game)
    
    def addGame(self, game):
        if type(game) == Game:
                self.games.append(game)
        elif type(game) == GameCollection:
            self.games.append(game)
        elif type(game) == tuple:
            if game[1]['type'] == 'game':
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
            return next(val for x, val in enumerate(self.games) if l(game, val))
        except Exception as e:
            print(str(e))
            return None
    
    def remove(self, game:Union[Game, 'GameCollection']):
        '''Removes the specified game from this game collection\n
        game: the game/collection to remove\n
        NOTE: raises exception if not in this collection
        '''
        self.games.remove(game)
    
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
        '''Returns true if self and obj are the same collection (only checks name on one local collection)'''
        if isinstance(obj, GameCollection):
            if len(self.games) != 0 and len(obj.games) != 0:
                return self.name == obj.name and len(self.games) == len(obj.games) and self.games == obj.games
            else:
                return self.name == obj.name
        return False

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
    
    def jsonify(self, online:bool = True):
        '''Returns a json representation of this game collection for saving purposes\n
        online: Should the json represent urls? Else prepare with local paths
        '''
        return {
        "type": "collection",
        "name": self.name,
        "games": {game.name : game.jsonify(online) for game in self.games}
        }
        
    def merge(self, other:'GameCollection'):
        '''Merges self and the other game collection. Takes information from other and merges into self.\n
        NOTE: If any games exist in both collections, other will be merged into self. If any exist not in other, it will be added as-is
        '''
        notin = []
        #TODO: gotta optimize this. Without sorting, this is gonna be at an n^2 algorithm
        for gother in other:
            found = False
            for game in self.games:
                #same, merge
                if game == gother:
                    #ducktype the merge, both game and gamecollection have this function
                    game.merge(gother)
                    found = True
            #after, if not found, add to notin list
            if not found:
                notin.append(gother)
        #extend list for all not in this game
        self.games.extend(notin)