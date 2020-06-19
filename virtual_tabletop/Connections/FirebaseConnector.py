import pyrebase, json, os
from virtual_tabletop.Data import Game, GameCollection

class Connector:
    '''A simple connector to Firestore via the Pyrebase wrapper API found: https://github.com/thisbejim/Pyrebase'''

    def __init__(self, key, cred = None, email=None, password=None, savedir = os.path.join('.','localboards')):
        '''Init method:\n
            key: API key JSON for your specific firebase instance\n
            cred: credentials JSON for your sign-in info, None by default\n
            For dev purposes, credentials will be stored in plaintext on user request. This should be changed to fit with Pyrebase login while preserving persistence in login state\n
            email: backup string email to sign in\n
            password: backup string password to sign in\n
            savedir: the location to save files to, defaults to a folder in this dir called localboards
        '''
        self.__config = json.load(open(key))
        self.__creds = None
        if cred:
            self.__creds = json.load(open(cred))
        elif email and password:
            self.__creds = {"email": email, "password": password}

        #set up current data and location in DB for local
        self.__data = None
        self.__location = ''
        self.__locationname = ''

        #configure pyrebase link
        self.__fb = pyrebase.initialize_app(self.__config)
        self.__auth = self.__fb.auth()
        self.__user = None 
        if self.__creds is not None:
            self.__user = self.__auth.sign_in_with_email_and_password(self.__creds['email'], self.__creds['password'])
        
        self.__db = self.__fb.database()
        self.__storage = self.__fb.storage()

        #get base data
        self._getLevel()
    
    def _getLevel(self):
        '''Gets the current level in the database and fills underlying data field'''
        data = self.__db.child(self.__location).get().val()

        #parse the data (must be as collection)
        self.__data = GameCollection.GameCollection(self.__locationname, data)

    def goUp(self):
        '''Goes up in the DB hierarchy'''
        #if we are at base, ignore, else strip the last "/~~~/games" from the location
        if self.__location != '':
            loc = self.__location.split('/')
            #NOTE, below will not break on python 3.7 as it treats it as an iterable from beginning until not less than 2 before end, so instantly stops
            loc = loc[:-2]
            self.__location = '/'.join(loc)
            self.__locationname = '' if len(loc) < 1 else loc[-1]
            self._getLevel()


    def goDown(self, name):
        '''Goes down in the DB hierarchy as given by new level "name"'''
        self.__location += name + '/games'
        self.__locationname = name
        self._getLevel()
    
    def add(self, toAdd, location = None):
        '''Adds a game or game collection to the given location:\n
        toAdd: a game or game collection to put into the DB\n
        location: the location to add to, defaults to current location
        '''
        #default location
        if location is None:
            location = self.__location.replace('games/','')
        
        #parse for valid object
        if type(toAdd) not in [Game, GameCollection]:
            raise TypeError('Invalid object type for DB save:\nExpected {0} or {1} but received {2}'.format(Game, GameCollection, type(toAdd)))

        #pre-iterate through to push images to DB
        self.__upload(toAdd, location)

        #good to go, jsonify and parse
        self.__db.child(location).child(toAdd.name).set(toAdd.jsonify())
    
    def __upload(self, toAdd, location):
        '''Uploads toAdd to the database, parsing all non-local games and securing a place in file storage for preview/board\n
        toAdd: the game/game collection to add
        location: the location to upload the board to
        NOTE: this is a recursive method that will iterate through game collections, thus callable with collections or single games
        '''
        if type(toAdd) == Game:
            #push to file storage
            # will be path: /Collection/.../name_board.jpg + name_preview.jpg
            #NOTE: ignoring file name as we will make our own via naming conventions above, just need extension
            board_type = os.path.splitext(toAdd.__board_path)[1]
            prev_type = os.path.splitext(toAdd.__preview_path)[1]
            self.__storage.child(location).child(toAdd.name + '_board' + board_type).put(toAdd.__board_path)
            self.__storage.child(location).child(toAdd.name + '_preview' + prev_type).put(toAdd.__board_path)

        elif type(toAdd) == GameCollection:
            #nothing to do for collections, iterate over each game with this name added to location
            loc = location + '/' + toAdd.name
            for game in toAdd:
                self.__upload(game, loc)
        else:
            raise TypeError('Invalid object type for image storage save:\nExpected {0} or {1} but received {2}'.format(Game, GameCollection, type(toAdd)))


