#!/usr/bin/python3

import html
import bottle
from models.users import users as USERS
from models.posts import posts as POSTS
from models.sessions import sessions as SESSIONS
from bottle import SimpleTemplate



app = bottle.Bottle()
SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/')
def blogIndex():
    '''
    The main page for the blog.
    '''

    cookie = bottle.request.get_cookie('session')

    username = SESSIONS.getUsername(cookie)

    posts = POSTS.getPosts(10)

    return bottle.template(
            'index',
            dict(posts=posts, username=username)
    )

@app.route('/tag/<tag>')
def postByTag(tag='notfound'):
    '''
    Posts filtered by tag.
    '''

    cookie = bottle.request.get_cookie('session')
    tag = html.escape(tag)

    username = SESSIONS.getUsername(cookie)

    posts = POSTS.getPostsByTag(tag, 10)

    return bottle.template(
            'index',
            dict(posts=posts, username=username)
    )

@app.get('/post/<permalink>')
def showPost(permalink):
    '''
    Specific post by permalink.
    '''

    cookie = bottle.request.get_cookie('session')

    username = SESSIONS.getUsername(cookie)
    post = POSTS.getPostByPermalink(html.escape(permalink))

    comment = {
        'name': '',
        'body': '',
        'email': ''
    }

    return bottle.template(
            'post',
            dict(
                post=post,
                username=username,
                errors='',
                comment=comment
            )
    )

@app.route('/<filename:path>', name='static')
def server_static(filename):
    '''
    Routing for static files.
    '''

    return bottle.static_file(
            filename,
            root='/Users/faisalusmani/Documents/blog/blog/views/'
    )

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
