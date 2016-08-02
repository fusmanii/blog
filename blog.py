#!/usr/bin/python3

import bottle
from models.users import users as USERS
from models.posts import posts as POSTS
from models.sessions import sessions as SESSIONS



@bottle.route('/')
def blog_index():
    '''
    The main page for the blog.
    '''

    cookie = bottle.request.get_cookie('session')

    username = SESSIONS.getUsername(cookie)

    posts = POSTS.getPosts(10)

    return bottle.template('index', dict(posts=posts, username=username))

@bottle.route('/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='/Users/faisalusmani/Documents/blog/blog/views/')

if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(host='localhost', port=8080)
