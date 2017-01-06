import random
import string
from utils.db import db

class Sessions:
    """ Session DAO. """

    def __init__(self, db):
        ''' (self, pymongo.Database) -> NoneType
        Constructor for this Session
        '''

        self.db = db
        self.sessions = db.sessions

    def startSession(self, username):
        ''' (Sessions, str) -> str or None
        Starts a new session by adding a new entry into the database for the given
        username
        '''

        session = {
                '_id': ''.join([random.choice(string.ascii_letters)
                    for i in range(32)]),
                'username': username
            }

        try:
            self.sessions.insert_one(session)
            return session['_id']
        except: pass

    def endSession(self, sessionId):
        ''' (Sessions, str) -> NoneType
        Ends the session by removing the session with sessionId from the database.
        '''

        self.sessions.delete_one({'_id': sessionId})

    def getSession(self, sessionId):
        ''' (Sessions, str) -> dict or None
        Returns the session from the database if exists.
        '''

        try:
            return self.sessions.find_one({'_id': sessionId})
        except: pass

    def getUsername(self, sessionId):
        ''' (Sessions, str) -> str
        Returns the username for the given session.
        '''

        session = self.getSession(sessionId)
        if session:
            print('session:', session)
            return session['username']

# import this instance
sessions = Sessions(db)
