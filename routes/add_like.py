from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User
from classes.likes import Likes

from database import mydb


add_like_app = Blueprint('add_like', __name__, static_folder="static", template_folder="templates")

@add_like_app.route('/add_like', methods=['POST'])
def add_like():
    dataA = request.form['whomLiked']
    dataB = request.form['postID']

    #user_id = whomID
    #session = whoID 

    #Prvo treba proveiti da li je korisnik vec lajkovao taj post...
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM likes WHERE post_postID = ? AND who_liked = ?'
    values = (dataB, session['id'])
    cursor.execute(sql, values)

    res = cursor.fetchall()

    if len(res) != 0:
        cursor = mydb.cursor(prepared = True)
        sql = 'DELETE FROM likes WHERE post_postID = ? AND who_liked = ?'
        values = (dataB, session['id'])
        cursor.execute(sql, values)
        mydb.commit()

        return 'OK'

    one_like = Likes(None, dataA, dataB, session['id'])
    one_like.add_like()

    mydb.commit()

    return 'OK'