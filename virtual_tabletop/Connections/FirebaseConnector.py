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
        self.__data = []
        self.__location = ''

        #configure pyrebase link
        self.__fb = pyrebase.initialize_app(self.__config)
        self.__auth = self.__fb.auth()
        self.__user = None 
        if self.__creds is not None:
            self.__user = self.__auth.sign_in_with_email_and_password(self.__creds['email'], self.__creds['password'])
        
        self.__db = self.__fb.database()