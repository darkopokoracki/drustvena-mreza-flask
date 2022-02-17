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

notifications_app  = Blueprint('notifications', __name__)

@notifications_app.route('/notifications', methods=['POST'])
def notifications():
    if request.method == 'POST':
        pass

    # Sta nam treba on informacija:
    