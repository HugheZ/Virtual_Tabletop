import pyrebase, json, os
from virtual_tabletop.Data import Game, GameCollection

class Connector:
    '''A simple connector to Firestore via the Pyrebase wrapper API found: https://github.com/thisbejim/Pyrebase'''

    def __init__(self, key, cred = None, savedir = os.path.join('.','localboards')):
        '''Init method:\n
            key: API key JSON for your specific firebase instance\n
            cred: credentials JSON for your sign-in info, None by default\n
            For dev purposes, credentials will be stored on first-time login and in plaintext. This should be changed to fit with Pyrebase login while preserving persistence in login state
        '''
        self.__config = json.load(open(key))
        self.__creds = None
        if cred:
            self.__creds = json.load(open(cred))

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

        #get base data TODO
    
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
