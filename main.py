from math import nan
from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify
from importlib_metadata import re
import mysql.connector
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
import os.path

from user import User
from post import Post
from likes import Likes
from comment import Comment

app = Flask(__name__)
app.config['SECRET_KEY'] = '27723dshhDJs!'
# app.config['UPLOAD_FOLDER'] = 'static/images'

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)


#Proba
@app.route('/index')
def index():
    return 'Hello world from index'


@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'home.html'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if len(session) > 0:
        return redirect(
            url_for('posts')
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
        url_for('posts')
    )


@app.route('/login', methods=['GET', 'POST'])
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
    

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if len(session) == 0:
        return redirect(
            url_for('login')
        )

    if len(session) == 0:
        return redirect(
            url_for('login')
        )

    app.config['UPLOAD_FOLDER'] = 'static/images/posts'

    if request.method == 'GET':
        return render_template(
            'create_post.html'
        )

    title = request.form['title']
    content = request.form['content']
    image = request.files['image']

    if len(title) == 0:
        return render_template(
            'create_post.html',
            title_error = 'Naslov je obavezan!'
        )

    if len(content) == 0:
        return render_template(
            'create_post.html',
            content_error = 'Sadrzaj je obavezan!'
        )

    #Za sada ce nam i slika biti obzvezna...
    if not image:
        return render_template(
            'create_post.html',
            image_error = 'Slika je obavezna!'
        )

    allowed_extensions = ['jpg', 'png', 'jpeg']

    #Splitujemo po tacki i uzimamo poslednju poziciu
    extension = image.filename.split('.')[-1]

    if image and extension in allowed_extensions:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return render_template(
            'create_post.html',
            extension_error = 'Ekstenzija nije dozvoljena!'
        )

    post = Post(None, title, content, image.filename, session['id'])
    post.add_post()
    mydb.commit()  #Moramo i ovde sacuvati da bi se relodovalo...

    return redirect(
        url_for('posts')
    )


@app.route('/posts')
def posts():
    if len(session) == 0:
        return redirect(
            url_for('login')
        )

    # Uzimamo sve postove iz baze
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM post'
    cursor.execute(sql)
    posts_res = cursor.fetchall()

    if posts_res == None:
        return 'Nema nijednog posta na ovoj aplikaciji...'

    n = len(posts_res)
    posts_res = list(posts_res)
    posts = []

    for i in range(n):
        posts_res[i] = dekodiraj(posts_res[i])
        post_id = posts_res[i][0]
        title = posts_res[i][1]
        content = posts_res[i][2]
        image = posts_res[i][3]
        userID = posts_res[i][4]

        post = Post(post_id, title, content, image, userID)
        posts.append(post)

    # Uzimamo sve usere iz baze
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM user'
    cursor.execute(sql)
    users_res = cursor.fetchall()

    if users_res == None:
        return 'Nema nijednog korisnika na ovoj aplikaciji...'

    n = len(users_res)
    users_res = list(users_res)
    users = []

    for i in range(n):
        users_res[i] = dekodiraj(users_res[i])
        user_id = users_res[i][0]
        firstname = users_res[i][1]
        lastname = users_res[i][2]
        email = users_res[i][3]
        username = users_res[i][4]
        password = users_res[i][5]
        profile_image = users_res[i][6]

        user = User(user_id, firstname, lastname, email, username, password, profile_image)
        users.append(user)


    # Treba nam pismeni podatak iz tabele user i iz tabele post
    # Tako da moramo da spojimo te tabele
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT post.title, user.firstName, user.last_name, user.profile_image, user.username FROM post INNER JOIN user ON post.user_uderID = user.uderID ORDER BY postID;'
    cursor.execute(sql)

    join_res = cursor.fetchall()

    n = len(join_res)
    join_res = list(join_res)

    for i in range(n):
        join_res[i] = dekodiraj(join_res[i])

    # join_res izgleda ovako:
    # [['title1', 'firstname1', 'lastname1', 'profile_image1', 'username1'], ['title2','firstname2', 'lastname2', 'profile_image2', 'username2']]
    m = len(posts)
    

    #Moramo da znamo broj lajkova za svaki post koliko ima
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT COUNT(likes.likeID), post.postID FROM likes RIGHT JOIN post ON likes.post_postID = post.postID GROUP BY post.postID;'
    cursor.execute(sql)
    likes_join = cursor.fetchall()

    a = len(likes_join)
    for i in range(a):
        likes_join[i] = dekodiraj(likes_join[i])


    #Moramo da znamo da li je ulogovano korisnik lajkovao odredjeni post
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT post_postID, who_liked from likes;'
    cursor.execute(sql)
    who_liked = cursor.fetchall()

    t = len(who_liked)
    for i in range(t):
        who_liked[i] = dekodiraj(who_liked[i])


    all_posts = [] #Ovo je ko je sve lajkovao jedan post...

    for i in range(len(posts_res)):
        one_post = []
        for j in range(len(who_liked)):
            if posts_res[i][0] == who_liked[j][0]:
                one_post.append(who_liked[j][1])
        all_posts.append(one_post)

    return render_template(
        'posts.html',
        posts = posts,
        users = users,
        m = m,
        join_res = join_res,
        likes_join = likes_join,
        all_posts = all_posts
    )


@app.route('/get_posts')
def get_posts():
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT post.postID, post.title, post.content, post.image, user.uderID, user.firstName, user.last_name, user.email, user.username, profile_image FROM post INNER JOIN user ON post.user_uderID = user.uderID ORDER BY postID;'
    cursor.execute(sql)
    join_res = cursor.fetchall()

    n = len(join_res)
    join_res = list(join_res)

    for i in range(n):
        join_res[i] = dekodiraj(join_res[i])

    # join_res izgleda ovako:
    # [['postID1', 'title1', 'content1', 'image1', 'userID1', 'firstname1', 'lastname1', 'email1', 'username1', 'profile_image1'], 
    # [['postID2', 'title2', 'content2', 'image2', 'userI2', 'firstname2', 'lastname2', 'email2', 'username2', 'profile_image2']]
    ##############################################

    #Moramo da znamo da li je ulogovano korisnik lajkovao odredjeni post
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT post_postID, who_liked from likes;'
    cursor.execute(sql)
    who_liked = cursor.fetchall()

    t = len(who_liked)
    for i in range(t):
        who_liked[i] = dekodiraj(who_liked[i])

    ###################################################
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT COUNT(likes.likeID), post.postID FROM likes RIGHT JOIN post ON likes.post_postID = post.postID GROUP BY post.postID;'
    cursor.execute(sql)
    likes_join = cursor.fetchall()

    a = len(likes_join)
    for i in range(a):
        likes_join[i] = dekodiraj(likes_join[i])

    all_posts = [] #Ovo je ko je sve lajkovao jedan post...

    for i in range(n):
        one_post = []
        for j in range(len(who_liked)):
            if join_res[i][0] == who_liked[j][0]:
                one_post.append(who_liked[j][1])
        all_posts.append(one_post)

    # Treba da formirao jsonify
    posts = []
    for i in range(n):
        post = {
            'postID': join_res[i][0],
            'title': join_res[i][1],
            'content': join_res[i][2],
            'image': join_res[i][3],
            'userID': join_res[i][4],
            'firstname': join_res[i][5],
            'lastname': join_res[i][6],
            'email': join_res[i][7],
            'username': join_res[i][8],
            'profile_image': join_res[i][9],
            'likes': likes_join[i][0],
            'currentUser': session['id'],
            'whoLiked': all_posts[i],
            'isLiked': None
        }

        posts.append(post)

    return jsonify(posts)



@app.route('/posts/<id>')
def post(id):
    cursor = mydb.cursor(prepared = True)
    

@app.route('/profile/<username>')
def profile(username):
    if len(session) == 0:
        return redirect(
            url_for('login')
        )

    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM user WHERE username = ?'
    values = (username, )
    cursor.execute(sql, values)

    res = cursor.fetchone()

    if res == None:
        return redirect(
            url_for('home')
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


@app.route('/logout')
def logout():
    if len(session) > 0:
        session.pop('username')
        session.pop('firstname')
        session.pop('lastname')
        session.pop('id')

        return redirect(
            url_for('login')
        )

    else:
        return redirect(
            url_for('register')
        )

@app.route('/add_like', methods=['POST'])
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


@app.route('/add_comment/<username>', methods=['POST'])
def add_comment(username):
    cursor = mydb.cursor(prepared = True)
    


def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data


@app.route('/edit/<username>', methods=['GET', 'POST'])
def edit(username):
    app.config['UPLOAD_FOLDER'] = 'static/images/profile' #Podesavamo folder gde cemo cuvati slike

    if request.method == 'GET':
        cursor = mydb.cursor(prepared = True)
        sql = 'SELECT * FROM user WHERE username = ?'
        values = (username, )
        cursor.execute(sql, values)

        res = cursor.fetchone()

        if res == None:
            return redirect(
                url_for('posts')
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
                profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
            url_for('profile', username = new_username)
        )

@app.route('/example')
def example():
    myData = {
        'firstname': 'Darko',
        'lastname': 'Pokoracki',
        'age': 20
    }

    return jsonify(myData)

app.run(debug = True)

