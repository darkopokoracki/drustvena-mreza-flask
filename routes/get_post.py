from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User

from database import mydb



get_post_app = Blueprint('get_post', __name__, static_folder="static", template_folder="templates")

@get_post_app.route('/get_post', methods=['GET', 'POST'])
def get_post():
    id = request.form['postID']

    # Upit za lajkove...
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT likes.post_postID, user.firstName, user.last_name, user.username, user.profile_image FROM likes INNER JOIN user ON likes.who_liked = user.uderID WHERE likes.post_postID = ?;'
    values = (id, )
    cursor.execute(sql, values)

    likes_res = cursor.fetchall()
    likes_res = list(likes_res)
    n = len(likes_res)

    for i in range(n):
        likes_res[i] = dekodiraj(likes_res[i])

    # return str(likes_res)
    likes = []  #Ovo ce nam biti lista sa recnicima...

    for i in range(n):
        like = {
            'firstname': likes_res[i][1],
            'lastname': likes_res[i][2],
            'username': likes_res[i][3],
            'profile_image': likes_res[i][4]
        }

        likes.append(like)
    

    # Upit za komentare...
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT comment.commentID, comment.content, user.firstName, user.last_name, user.username, user.profile_image FROM comment INNER JOIN user ON comment.user_uderID = user.uderID WHERE comment.post_postID = ?;'
    values = (id, )
    cursor.execute(sql, values)

    comments_res = cursor.fetchall()
    n = len(comments_res)
    comments_res = list(comments_res)

    for i in range(n):
        comments_res[i] = dekodiraj(comments_res[i])

    comments = []

    for i in range(n):
        comment = {
            'content': comments_res[i][1],
            'firstname': comments_res[i][2],
            'lastname': comments_res[i][3],
            'username': comments_res[i][4],
            'profile_image': comments_res[i][5]
        }
        comments.append(comment)
    
    likes_comments_data = [likes, comments]

    return jsonify(likes_comments_data)

def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data