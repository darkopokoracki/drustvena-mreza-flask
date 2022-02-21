from calendar import c
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User
from routes.posts import posts

from database import mydb


post_app = Blueprint('post', __name__, static_folder="static", template_folder="template")

@post_app.route('/post/<id>')
def post(id):
    if len(session) == 0:
        return redirect(
            url_for('home.home')
        )
    
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM post WHERE postID = ?'
    values = (id, )
    cursor.execute(sql, values)

    post_res = cursor.fetchone()

    if post_res == None:
        return redirect(
            url_for('posts.posts')
        )

    post_res = dekodiraj(post_res)
    
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT post.postID, post.title, post.content, post.image, user.firstName, user.last_name, user.username, user.email, user.profile_image, user.uderID FROM post INNER JOIN user ON post.user_uderID = user.uderID WHERE postID = ?;'
    values = (id, )
    cursor.execute(sql, values)
    post_user_res = cursor.fetchone()

    post_user_res = dekodiraj(post_user_res)
    # return str(post_user_res)


    #Dohvatamo ko je lajkovao
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT who_liked FROM likes WHERE post_postID = ?'
    values = (id, )
    cursor.execute(sql, values)

    who_liked_res = cursor.fetchall()

    m = len(who_liked_res)
    who_liked_res = list(who_liked_res)

    for i in range(m):
        who_liked_res[i] = dekodiraj(who_liked_res[i])

    who_liked = [item for sublist in who_liked_res for item in sublist]

    # return str(post_user_res)
    if request.method == 'GET': 
        return render_template(
            'post.html',
            post_user_res = post_user_res,
            who_liked = who_liked
        )
    


def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data