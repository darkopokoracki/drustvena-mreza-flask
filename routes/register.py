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

register_app = Blueprint('register', __name__, static_folder="static", template_folder="templates")

@register_app.route('/register', methods=['GET', 'POST'])
def register():
    if len(session) > 0:
        return redirect(
            url_for('posts.posts')
        )

    if request.method == 'GET':
        return render_template(
            'register.html'
        )

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']

    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM user WHERE email = ? OR username = ?'
    values = (email, username)
    cursor.execute(sql, values)

    res = cursor.fetchone()

    if res != None:
        return render_template(
            'register.html',
            acc_error = 'Takav nalog vec postoji!'
        )

    if len(firstname) < 2:
        return render_template(
            'register.html',
            firstname_error = 'Ime mora imati najmanje 2 karaktera!'
        )

    if len(lastname) < 2:
        return render_template(
            'register.html',
            lastname_error = 'Prezime mora imati najmanje 2 karaktera!'
        )

    if len(username) < 2:
        return render_template(
            'register.html',
            username_error = 'Username ne sme biti kraci od 2 karaktera!'
        )

    if len(password) < 6:
        return render_template(
            'register.html',
            password_error = 'Lozinka mora imati najmanje 6 karaktera!'
        )

    if password != confirm:
        return render_template(
            'register.html',
            confirm_error = 'Lozinke se ne poklapaju!'
        )
    
    user = User(None, firstname, lastname, email, username, password, 'default.png')
    user.register() #Registrujemo korisnika pomocu metode u klasi
    mydb.commit()

    return redirect(
        url_for('posts.posts')
    )