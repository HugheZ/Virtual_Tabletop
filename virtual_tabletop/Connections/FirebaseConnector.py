import pyrebase, json, glob
from os import path, mkdir, makedirs
from shutil import copyfile
from virtual_tabletop.Data.Game import Game 
from virtual_tabletop.Data.GameCollection import GameCollection
from weakref import ref, WeakMethod
from typing import Callable, Mapping, Union, Optional

class Connector:
    '''A simple connector to Firestore via the Pyrebase wrapper API found: https://github.com/thisbejim/Pyrebase'''

    def __init__(self, key: Union[str, Mapping], savedir: str = path.join('.','localboards')):
        '''Init method:\n
            key: API key JSON for your specific firebase instance\n
            email: backup string email to sign in\n
            password: backup string password to sign in\n
            savedir: the location to save files to, defaults to a folder in this dir called localboards
        '''

        #get default config
        if type(key) == str:
            with open(key) as f:
                self.__config = json.load(f)
        elif type(key) == Mapping:
            self.__config == key

        #set up current data and location in DB for local
        self.__data = None
        #physical location
        self.__location = ''
        #location ending
        self.__locationname = ''
        #get local default save location
        self.__savedir = savedir

        #configure pyrebase link
        self.__fb = pyrebase.initialize_app(self.__config)
        self.__auth = self.__fb.auth()
        self.__user = None 
        
        self.__db = self.__fb.database()
        self.__storage = self.__fb.storage()

        #set updators
        self.__watchers = []
    
    def login(self, email: str, password: str):
        '''Logs into the linked DB and gets initial data\n
        email: the email used to log in\n
        password: the password used to log in
        '''
        if email and password:
            self.__user = self.__auth.sign_in_with_email_and_password(email, password)
    
    def logout(self):
        '''Logs out of the linked DB, resets data
        '''
        self.__auth.current_user = None
        self.__user = None
        self.__data = None
        self.__location = ''
        self.__locationname = ''
        self._getLevel()
    
    def isLoggedIn(self):
        '''Returns true if the current user is logged in, else false
        '''
        return self.__auth.current_user is not None and self.__user is not None
    
    def getLocation(self):
        '''Gets the human-readable location for the currently loaded level
        '''
        return self.__location.replace('/games', '')

    def _getLevel(self, echo:bool = False):
        '''Gets the current level in the database and fills underlying data field\n
        echo: boolean used to determine if the error message should echo. Should only be used on first-get to avoid annoying users
        '''
        onlineData = None
        localData = None
        err = None
        try:
            #NOTE: have to specify ID token. Pyrebase has an error that if you log out or log in after setting
            #up databases, you'll have to specify this. I tried remaking all objects, but NOOOOO, it doesn't work.
            #the code has a few smells with sharing information, but similar issues have been open for years so we
            #will just have to deal with this.
            data = self.__fb.database().child(self.__location).get(self.__user['idToken']).val()

            #parse the data (must be as collection)
            onlineData = GameCollection(self.__locationname, data)
        except Exception as e:
            err = e
            self.__data = None

        #set up blank game collection for this level local
        localData = GameCollection(self.__locationname)
        #get all json files at ~savedir~/self.getLocation() and iterate
        for jsn in glob.iglob(path.join(self.__savedir, self.getLocation(), '*.json')):
            try:
                with open(jsn) as f:
                    data = json.load(f)
                    try: #try to parse and load each json, skipping if it can't be parsed
                        game = Game(data['name'], data['width'], data['height'], data['preview_image'], data['board'], True, False)
                        localData.addGame(game)
                    except:
                        print('Failed to parse game json')
            except:
                print('Failed to open json')

        #merge if online data is retrieved and set data to the emrged set
        if onlineData is not None:
            onlineData.merge(localData)
            self.__data = onlineData
        else:
            self.__data = localData

        #notify any watcher
        self.__updateWatchers()

        #send error notification if requested
        if echo and err:
            raise err
    
    def refresh(self, echo:bool = False):
        '''Publicly visible refresh method to update pulled data\n
        echo: whether to echo error details
        '''
        self._getLevel(echo)

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


    def goDown(self, name: str):
        '''Goes down in the DB hierarchy\n
        name: the new level to go down to
        '''
        self.__location += name + '/games'
        self.__locationname = name
        self._getLevel()

    def addToLocal(self, toAdd: Union[Game, GameCollection], location: Optional[str] = None):
        '''Saves the game or game collection to the given location in local storage\n
        toAdd: a game or game collection to save\n
        location: the location to add to, defaults to current location
        '''
        #get human readable location
        if location is None:
            location = path.join(self.__savedir, self.getLocation())
            print(location)
        
        #if game or collection, save differently, else throw error
        if isinstance(toAdd, Game):
            #create all directories if they don't exist
            makedirs(location, exist_ok=True)
            #move images to local storage location, then save jsonified object
            oldBoard = toAdd.getBoardPath(False)
            oldPreview = toAdd.getPreviewPath(False)
            #move and copy board
            obtype = path.splitext(oldBoard)[1]
            newBoard = path.join(location, toAdd.name + '_board' + obtype)
            copyfile(oldBoard, newBoard)
            #now preview, skip moving if no preview is given
            optype = None
            newPreview = None
            if oldPreview is not None:
                optype = path.splitext(oldPreview)[1]
                newPreview = path.join(location, toAdd.name + '_preview' + optype)
                copyfile(oldPreview, newPreview)
            #update game
            toAdd.setBoardPath(newBoard, False)
            toAdd.setPreviewPath(newPreview, False)
            #save jsonified value
            jsfpth = path.join(location, toAdd.name + '.json')
            print(jsfpth)
            with open(jsfpth, 'w+') as f:
                json.dump(toAdd.jsonify(False), f)
        elif isinstance(toAdd, GameCollection):
            #save the collection as a folder in local directory, recurse for all games in collection
            #create directory
            direc = path.join(location, toAdd.name)
            try:
                mkdir(direc)
            except FileExistsError:
                pass
            except:
                raise
            #call save to all children
            for game in toAdd:
                self.addToLocal(game, direc)
        else:
            raise TypeError('Invalid object type for DB save:\nExpected {0} or {1} but received {2}'.format(Game, GameCollection, type(toAdd)))
    
    def addToCloud(self, toAdd: Union[Game, GameCollection], location: Optional[str] = None):
        '''Adds a game or game collection to the given location in the cloud:\n
        toAdd: a game or game collection to put into the DB\n
        location: the location to add to, defaults to current location
        '''
        #default location
        if location is None:
            location = self.__location#.replace('games/','')
        
        #parse for valid object
        if type(toAdd) not in [Game, GameCollection]:
            raise TypeError('Invalid object type for DB save:\nExpected {0} or {1} but received {2}'.format(Game, GameCollection, type(toAdd)))

        #pre-iterate through to push images to DB
        self.__upload(toAdd, location)

        #good to go, jsonify and parse
        self.__db.child(location).child(toAdd.name).set(toAdd.jsonify(True), self.__user['idToken'])
    
    def __upload(self, toAdd: Union[Game, GameCollection], location: str):
        '''Uploads toAdd to the database, parsing all non-local games and securing a place in file storage for preview/board\n
        toAdd: the game/game collection to add\n
        location: the location to upload the board to\n
        NOTE: this is a recursive method that will iterate through game collections, thus callable with collections or single games
        '''
        if type(toAdd) == Game:
            #push to file storage
            # will be path: /Collection/.../name_board.jpg + name_preview.jpg
            #NOTE: ignoring file name as we will make our own via naming conventions above, just need extension
            board_type = path.splitext(toAdd.getBoardPath(False))[1]
            prev_type = path.splitext(toAdd.getBoardPath(False))[1]
            boardPath = toAdd.name + '_board' + board_type
            previewPath = toAdd.name + '_preview' + prev_type
            self.__storage.child(location).child(boardPath).put(toAdd.getBoardPath(False), self.__user['idToken'])
            self.__storage.child(location).child(previewPath).put(toAdd.getPreviewPath(False), self.__user['idToken'])
            #after push, retain new http endpoint to pull images from
            boardUrl = self.__storage.child(location).child(boardPath).get_url(self.__user['idToken'])
            previewUrl = self.__storage.child(location).child(previewPath).get_url(self.__user['idToken'])
            toAdd.setBoardPath(boardUrl, True)
            toAdd.setPreviewPath(previewUrl, True)

        elif type(toAdd) == GameCollection:
            #nothing to do for collections, iterate over each game with this name added to location
            loc = location + '/' + toAdd.name
            for game in toAdd:
                self.__upload(game, loc)
        else:
            raise TypeError('Invalid object type for image storage save:\nExpected {0} or {1} but received {2}'.format(Game, GameCollection, type(toAdd)))
    
    def watch(self, caller: Optional[object] = None, callback: Optional[Callable] = None):
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
    
    def unwatch(self, obj: object):
        '''Removes the provided object from the watchers list, excepting if it was not present.\n
        obj: the object to be removed from the watcher list
        '''
        try:
            next(x for x, val in enumerate(self.__watchers) if val[0]() == obj)
        except Exception:
            raise IndexError('Object to remove from watchers was not watching')
        return
