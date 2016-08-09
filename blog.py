#!/usr/bin/python3

import html
import bottle
from models.users import users as USERS
from models.posts import posts as POSTS
from models.sessions import sessions as SESSIONS

app = bottle.Bottle()

@app.route('/')
def blogIndex():
    '''
    The main page for the blog.
    '''

    cookie = bottle.request.get_cookie('session')

    username = SESSIONS.getUsername(cookie)

    posts = POSTS.getPosts(10)

    return bottle.template('index', dict(
            posts=posts, username=username, get_url=app.get_url))

@app.route('/tag/<tag>')
def postByTag(tag='notfound'):
    '''
    Posts filtered by tag.
    '''

    cookie = bottle.request.get_cookie('session')
    tag = html.escape(tag)

    username = SESSIONS.getUsername(cookie)

    posts = POSTS.getPostsByTag(tag, 10)

    return bottle.template('index', dict(posts=posts, username=username, get_url=app.get_url))

@app.route('/<filename:path>', name='static')
def server_static(filename):
    '''
    Routing for css and js files.
    '''
    print(filename)
    return bottle.static_file(filename, root='/Users/faisalusmani/Documents/blog/blog/views/')

if __name__ == '__main__':
    #bottle.debug(True)
    app.run(host='localhost', port=8000, debug=True)
