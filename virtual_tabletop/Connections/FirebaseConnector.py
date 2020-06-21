import pyrebase, json, os
from virtual_tabletop.Data import Game, GameCollection
from weakref import ref, WeakMethod

class Connector:
    '''A simple connector to Firestore via the Pyrebase wrapper API found: https://github.com/thisbejim/Pyrebase'''

    def __init__(self, key, email=None, password=None, savedir = os.path.join('.','localboards')):
        '''Init method:\n
            key: API key JSON for your specific firebase instance\n
            email: backup string email to sign in\n
            password: backup string password to sign in\n
            savedir: the location to save files to, defaults to a folder in this dir called localboards
        '''
        self.__config = json.load(open(key))

        #set up current data and location in DB for local
        self.__data = None
        self.__location = ''
        self.__locationname = ''

        #configure pyrebase link
        self.__fb = pyrebase.initialize_app(self.__config)
        self.__auth = self.__fb.auth()
        self.__user = None 
        
        #login
        self.login(email, password)
        
        self.__db = self.__fb.database()
        self.__storage = self.__fb.storage()

        #get base data
        self._getLevel()

        #set updators
        self.__watchers = []
    
    def login(self, email, password):
        '''Logs into the linked DB\n
        email: the email used to log in\n
        password: the password used to log in
        '''
        if email and password:
            self.__user = self.__auth.sign_in_with_email_and_password(email, password)
    
    def _getLevel(self):
        '''Gets the current level in the database and fills underlying data field'''
        data = self.__db.child(self.__location).get().val()

        #parse the data (must be as collection)
        self.__data = GameCollection.GameCollection(self.__locationname, data)

        #notify any watcher
        self.__updateWatchers()

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
    
    def watch(self, caller=None, callback=None):
        '''Observer-like function that updates the currently loaded DB data. All callbacks are called immediately upon addition.\n
        caller: the object owning the callback, used to keep track and remove watchers\n
        callback: an optional callback to call whenever the pulled data is updated, of the form:\n
        \tfunc( GameCollection ) → any\n
        Returns the most up-to-date DB data as a one-time look
        '''
        #error out if callback and no caller or vice versa
        if caller and not callback or callback and not caller:
            raise ValueError('Both caller and callback must be defined for watching')

        #try to add callback if exists, throw error if non-callable given
        if callback and caller:
            if callable(callback):
                self.__watchers.append((ref(caller), WeakMethod(callback)))
                callback(self.__data)
            else:
                raise TypeError('Callback given is not callable')
        
        #give static copy
        return self.__data
    
    def __updateWatchers(self):
        '''Updates all current data watchers. If a watcher is dead, this will remove it from this and future updates.'''
        rmlist = []
        for i in range(len(self.__watchers)):
            watcher = self.__watchers[i]
            watcher_obj = watcher[0]()
            watcher_func = watcher[1]()
            if watcher_obj:
                watcher_func(self.__data)
            else:
                #dead reference, add to remove list
                rmlist.append(i)
        
        #remove all dead watchers
        for rm in rmlist:
            del self.__watchers[rm]
    
    def unwatch(self, obj):
        '''Removes the provided object from the watchers list, excepting if it was not present.\n
        obj: the object to be removed from the watcher list
        '''
        try:
            next(x for x, val in enumerate(self.__watchers) if val[0]() == obj)
        except Exception:
            raise IndexError('Object to remove from watchers was not watching')
        return
