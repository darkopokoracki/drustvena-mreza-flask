from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, current_app
from passlib.hash import sha256_crypt
from classes.user import User
import mysql.connector
import os.path
from werkzeug.utils import secure_filename

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)

edit_app = Blueprint('edit', __name__, static_folder="static", template_folder="templates")

@edit_app.route('/edit/<username>', methods=['GET', 'POST'])
def edit(username):
    current_app.config['UPLOAD_FOLDER'] = 'static/images/profile' #Podesavamo folder gde cemo cuvati slike

    if request.method == 'GET':
        cursor = mydb.cursor(prepared = True)
        sql = 'SELECT * FROM user WHERE username = ?'
        values = (username, )
        cursor.execute(sql, values)

        res = cursor.fetchone()

        if res == None:
            return redirect(
                url_for('posts.posts')
            )
    
        res = dekodiraj(res)
        user = User(res[0], res[1], res[2], res[3], res[4], res[5], res[6])

        return render_template(
            'edit.html',
            user = user
        )

    if request.method == 'POST':
        cursor = mydb.cursor(prepared = True)
        sql = 'SELECT * FROM user WHERE username = ?'
        values = (username, )
        cursor.execute(sql, values)

        res = cursor.fetchone()

        res = dekodiraj(res)
        user = User(res[0], res[1], res[2], res[3], res[4], res[5], res[6])

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        new_username = request.form['username']
        profile_picture = request.files['profile_picture']

        allowed_extensions = ['jpg', 'png', 'jpeg']

        if not profile_picture:
            profile_picture = res[6]
            extension = profile_picture.split('.')[-1]

        else:
            extension = profile_picture.filename.split('.')[-1]
        
            if profile_picture and extension in allowed_extensions:
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(edit_app.config['UPLOAD_FOLDER'], filename))
            else:
                return render_template (
                    'edit.html',
                    user = user,
                    extension_error = 'Ekstenzija nije dozvoljena!'
                )
            
            profile_picture = profile_picture.filename

        # return str(user)
        #Validacija...
        if len(firstname) < 2:
            return render_template(
                'edit.html',
                user = user,
                firstname_error = 'Ime mora imati najmanje 2 karaktera!'
            )

        if len(lastname) < 2:
            return render_template(
                'edit.html',
                user = user,
                lastname_error = 'Prezime mora imati najmanje 2 karaktera!'
            )

        if len(new_username) < 2:
            return render_template(
                'edit.html',
                user = user,
                username_error = 'Username mora imati najmanje 2 karaktera!'
            )

        #Moramo proveriti da li vec neko ima ovaj username u bazi
        my_cursor = mydb.cursor(prepared = True)
        sql = 'SELECT * FROM user WHERE username = ? AND uderID <> ?'
        values = (new_username, user.get_id())
        my_cursor.execute(sql, values)

        my_res = my_cursor.fetchone()

        if my_res != None:
            return render_template(
                'edit.html',
                user = user,
                username_exists_error = 'Username je zauzet'
            )

        user.set_firstname(firstname)
        user.set_lastname(lastname)
        user.set_username(new_username)
        user.set_profile_image(profile_picture)

        user.update()
        mydb.commit()

        return redirect(
            url_for('profile.profile', username = new_username)
        )

def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data