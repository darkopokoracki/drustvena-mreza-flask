from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User

from database import mydb



get_post_app = Blueprint('get_post', __name__, static_folder="static", template_folder="templates")

@get_post_app.route('/get_post', methods=['GET', 'POST'])
def get_post():
    id = request.form['postID']

    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT likes.post_postID, user.firstName, user.last_name, user.username, user.profile_image FROM likes INNER JOIN user ON likes.who_liked = user.uderID WHERE likes.post_postID = ?;'
    values = (id, )
    cursor.execute(sql, values)

    res = cursor.fetchall()
    res = list(res)
    n = len(res)

    for i in range(n):
        res[i] = dekodiraj(res[i])

    # return str(res)
    likes = []  #Ovo ce nam biti lista sa recnicima...

    for i in range(n):
        like = {
            'firstname': res[i][1],
            'lastname': res[i][2],
            'username': res[i][3],
            'profile_image': res[i][4]
        }

        likes.append(like)
    
    return jsonify(likes)

def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data