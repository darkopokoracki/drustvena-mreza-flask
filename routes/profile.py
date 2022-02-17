from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User
import mysql.connector
from classes.post import Post

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)

profile_app = Blueprint('profile', __name__, static_folder="static", template_folder="templates")

@profile_app.route('/profile/<username>')
def profile(username):
    if len(session) == 0:
        return redirect(
            url_for('login.login')
        )

    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM user WHERE username = ?'
    values = (username, )
    cursor.execute(sql, values)

    res = cursor.fetchone()

    if res == None:
        return redirect(
            url_for('home.hom')
        )

    res = dekodiraj(res)

    user_id = res[0]
    firstname = res[1]
    lastname = res[2]
    email = res[3]
    username = res[4]
    password = res[5]
    profile_image = res[6]

    user = User(user_id, firstname, lastname, email, username, password, profile_image)

    post_cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM post WHERE user_uderID = ?;'
    values = (user.get_id(), )
    post_cursor.execute(sql, values)

    post_res = post_cursor.fetchall()

    n = len(post_res)
    post_res = list(post_res)
    
    all_posts = []
    # return str(post_res[0])
    for i in range(n):
        post_res[i] = dekodiraj(post_res[i])

        post_id = post_res[i][0]
        title = post_res[i][1]
        content = post_res[i][2]
        image = post_res[i][3]
        userID = post_res[i][4]

        post = Post(post_id, title, content, image, userID)
        all_posts.append(post)

    return render_template(
        'profile.html',
        user = user,
        posts = all_posts
    )

def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data