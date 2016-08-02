import pymongo
import string
import hashlib
import random
from utils.db import db

class Users:
    """ Users DAO. """

    def __init__(self, db):
        ''' (Users, pymongo.Database) -> NoneType
        Constructor for this User.
        '''

        self.db = db
        self.users = db.users

    def validate(self, username, password):
        ''' (Users, str, str) -> dict or None
        Returns the user record if the user login validates, None otherwise.
        '''

        try:
            user = self.users.find_one({'_id': username})

            if user and user['password'] == self._getHash(
                    password,
                    user['password'].split(':')[1]
            ):
                return user
        except:
            pass

    def addUser(self, username, password, email):
        ''' (Users, str, str, str) -> bool
        Creates a new user in the database.
        '''

        user = {
            '_id': username,
            'password': self._getHash(password)
        }
        if email:
            user['email'] = email

        try:
            self.users.insert_one(user)
            return True
        except:
            pass

    def _getHash(self, password, _salt=None):
        ''' (Users, str, str) -> str
        Returns the sha256 hash of password with the salt if given. Generates
        a random salt if salt not present.
        '''

        if not _salt:
            _salt = ''.join([random.choice(string.ascii_letters)
                for i in range(5)])
        return hashlib.sha256(password + _salt).hexdigest() + ':' + _salt

# import this instance
users = Users(db)
