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

logout_app = Blueprint('logout', __name__)

@logout_app.route('/logout')
def logout():
    if len(session) > 0:
        session.pop('username')
        session.pop('firstname')
        session.pop('lastname')
        session.pop('id')
        session.pop('picture')

        return redirect(
            url_for('login.login')
        )

    else:
        return redirect(
            url_for('register.register')
        )