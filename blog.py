#!/usr/bin/python3

import html
import bottle
from models.users import users as USERS
from models.posts import posts as POSTS
from models.sessions import sessions as SESSIONS
from bottle import SimpleTemplate
import time



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

@app.post('/newcomment')
def postNewComment():
    '''
    Route for posting new comment for a given post.
    '''

    name = bottle.request.forms.get("name")
    email = bottle.request.forms.get("email")
    body = bottle.request.forms.get("message")
    permalink = bottle.request.forms.get("permalink")
    
    post = POSTS.getPostByPermalink(permalink)

    # if post not found, redirect to post not found error
    if not post:
        bottle.redirect("/post_not_found")
        return

    # all fields should be present
    POSTS.addComment(permalink, name, email, body)
    bottle.redirect("/post/" + permalink)

@app.post('/like')
def postCommentLike():
    '''
    Used to process a like on a blog post
    '''

    permalink = html.escape(bottle.request.forms.get("permalink"))
    commentOrdinal = int(bottle.request.forms.get("commentOrdinal"))

    post = POSTS.getPostByPermalink(permalink)
    POSTS.incrementLikes(permalink, commentOrdinal)
    bottle.redirect("/post/" + permalink)


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
    app.run(host='127.0.0.1', port=8080, debug=True, reloader=True)
