import datetime
import re
from utils.db import db


class Posts:
    """ Posts DAO. """

    def __init__(self, db):
        ''' (Posts, pymongo.Database) -> NoneType
        Constructor for this Posts
        '''

        self.db = db
        self.posts = db.posts

    def insert(self, title, post, tagsList, author):
        ''' (Posts, str, str, list, str) -> str
        Inserts a new post into the database and returns the pemalink for
        the entry.
        '''

        # create a permalink from the title by removing whitespaces
        # and non-alphanumeric charecters

        permalink = re.compile('\W').sub(
                '',
                re.compile('\s').sub('_', title)
            )

        post = {
            'title': title,
            'author': author,
            'body': post,
            'permalink': permalink,
            'tags': tagsList,
            'comments': [],
            'date': datetime.datetime.utcnow()
        }

        try:
            self.posts.insert_one(post)
        except: pass

        return permalink

    def getPosts(self, numPosts):
        ''' (Posts, int) -> list of dict
        Return a list of posts containing numPosts posts.
        '''

        return self._processPosts(self.posts.find().sort(
                'date',
                direction=-1
            ).limit(numPosts)
        )

    def getPostsByTag(self, tag, numPosts):
        ''' (Posts, str, int) -> list of dict
        Returns a list of posts with the given tag.
        '''

        return self._processPosts(self.posts.find({
                'tags': tag
            }).sort(
                'date',
                direction=-1
            ).limit(numPosts)
        )

    def getPostByPermalink(self, permalink):
        ''' (Posts, str) -> dict
        Returns the post with the permalink permalink.
        '''

        post = self.posts.find_one({'permalink': permalink})
        if post:
            for comment in post['comments']:
                if 'numLikes' not in comment:
                    comment['numLikes'] = 0
                elif isinstance(comment['numLikes'], float):
                    comment['numLikes'] = int(comment['numLikes'])

            post['date'] = post['date'].strftime('%A, %B %d %Y at %I:%M%p')

        return post

    def addComment(self, permalink, name, email, body):
        ''' (Posts, str, str, str, str) -> int
        Adds a comment for post with permalink.
        '''

        comment = {
                'author': name,
                'body': body
            }
        if email:
            comment['email'] = email

        try:
            response = self.posts.update_one(
                    {'permalink': permalink},
                    {'$push': {'comments': comment}}
                )
            return response.modiefied_count
        except:
            return 0

    def incrementLikes(self, permalink, commentOrdinal):
        ''' (Posts, str, int) -> int
        Increments the number of likes for post with permalink.
        '''

        return self.posts.update_one(
                {'permalink': permalink},
                {'$inc': {
                        'comments.%d.numLikes' % commentOrdinal: 1
                    }}
                ).modified_count

    def _processPosts(self, posts):
        ''' (Posts, pymongo.Cursor) -> list of dict
        Returns a list containing the posts from the cursor posts.
        '''

        return [{
                'title': post['title'],
                'body': post['body'],
                'date': post['date'].strftime('%A, %B %d %Y at %I:%M%p'),
                'permalink': post['permalink'],
                'tags': post.get('tags', []),
                'author': post['author'],
                'comments': post.get('comments', [])
            } for post in posts
        ]

# import this instance
posts = Posts(db)
