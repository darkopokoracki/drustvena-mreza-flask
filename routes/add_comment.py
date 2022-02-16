from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User
import mysql.connector

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)

add_comment_app = Blueprint('add_comment', __name__, static_folder="static", template_folder="templates")

@add_comment_app.route('/add_comment', methods=['POST'])
def add_comment():
    content = request.form['content']
    postID = request.form['postID']

    cursor = mydb.cursor(prepared = True)
    sql = 'INSERT INTO comment VALUES(null, ?, ?, ?)'
    values = (content, postID, session['id'])
    cursor.execute(sql, values)
    mydb.commit()