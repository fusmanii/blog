#!/usr/bin/python3

import html
import re
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

@app.get('/newpost')
def getNewPost():
    '''
    Displays the form allowing a user to add a new post. Only works for
    logged-in users.
    '''

    cookie = bottle.request.get_cookie("session")
    username = SESSIONS.get_username(cookie)  # see if user is logged in
    if not username:
        bottle.redirect("/login")

    return bottle.template("newpost_template",
                           {
                                "subject": "",
                                "body": "",
                                "errors": "",
                                "tags": "",
                                "username": username
                            }
                    )


@app.get('/signup')
def presentSignUp():
    '''
    Displays the initial blog signup form.
    '''

    return bottle.template("signup",
                           {
                                "username": "",
                                "password": "",
                                "password_error": "",
                                "email": "",
                                "username_error": "",
                                "email_error": "",
                                "verify_error": ""
                            }
                    )

@app.post('/signup')
def processSignUp():
    '''
    Processes the information entered in the signup form.
    '''

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verifypassword")
    print('username:', username, 'password:', password, 'verify:', verify, 'email:', email)
    print('equal', password == verify)

    errors = {
        'username': html.escape(username),
        'email': html.escape(email),
        "password_error": "",
        "username_error": "",
        "email_error": "",
        "verify_error": ""

    }
    if validateSignUp(username, password, verify, email, errors):

        if not users.addUser(username, password, email):
            # this was a duplicate
            errors['username_error'] = "Username already in use. \
                                        Please choose another username."
            return bottle.template("signup", errors)

        sessionId = sessions.start_session(username)
        bottle.response.set_cookie("session", sessionId)
        bottle.redirect("/")
    else:
        return bottle.template("signup", errors)

@app.route('/<filename:path>', name='static')
def server_static(filename):
    '''
    Routing for static files.
    '''

    return bottle.static_file(
            filename,
            root='/Users/faisalusmani/Documents/blog/blog/views/'
    )

# helpers
def validateSignUp(username, password, verify, email, errors):
    '''
    Validates the signup fields:
        - username length is 3-20 and contains only char, numbers, _, and -
        - password length is 3-20 char
        - password is the same as varify
        - email (if present) is proper format
    '''

    verified = True

    # setup the regexes
    userRegex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    passRegex = re.compile(r"^.{3,20}$")
    emailRegex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    if not userRegex.match(username):
        errors['username_error'] = "Invalid Username. \
            \n Username can contain letters, numbers, _, and -"
        verified = False

    if not passRegex.match(password):
        errors['password_error'] = "Invalid password. \
            \n Password must be between 3-20 characters long."
        verified = False

    if password != verify:
        errors['verify_error'] = "Passwords must match."
        verified = False

    if email and not emailRegex.mathc(email):
        errors['email_error'] = "Invalid email address."
        verified = False

    return verified


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, reloader=False)
