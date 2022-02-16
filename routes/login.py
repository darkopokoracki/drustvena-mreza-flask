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

login_app = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login_app.route('/login', methods=['GET', 'POST'])
def login():
    if len(session) > 0:
        return redirect(
            url_for('posts')
        )

    if request.method == 'GET':
        return render_template(
            'login.html'
        )
    
    #Koristimo email ili username za prijavu
    email_username = request.form['email_username']
    password = request.form['password']

    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM user WHERE email = ? OR username = ?'
    values = (email_username, email_username)
    cursor.execute(sql, values)

    res = cursor.fetchone()

    if res == None:
        return render_template(
            'login.html',
            email_username_error = 'Nalog ne postoji!'
        )

    res = dekodiraj(res)

    if (sha256_crypt.verify(password, res[5])) == False:
        return render_template(
            'login.html',
            password_error = 'Pogresna lozinka'
        )

    user = User(res[0], res[1], res[2], res[3], res[4], res[5], res[6])

    user.login() #Loginujemo korisnika pomocu metode u klasi User

    return redirect(
        url_for('posts')
    )

def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data