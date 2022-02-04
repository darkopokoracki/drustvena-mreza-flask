from flask import Flask, render_template, request, redirect, url_for, session
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


@app.route('/posts/<id>')
def post(id):
    cursor = mydb.cursor(prepared = True)
    


@app.route('/profile/<username>')
def profile(username):
    
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
    
    return render_template(
        'profile.html',
        user = user
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

@app.route('/add_like/<user_id>/<post_id>', methods=['POST'])
def add_like(user_id, post_id):

    #user_id = whomID
    #session = whoID 

    #Prvo treba proveiti da li je korisnik vec lajkovao taj post...
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM likes WHERE post_postID = ? AND who_liked = ?'
    values = (post_id, session['id'])
    cursor.execute(sql, values)

    res = cursor.fetchall()

    if len(res) != 0:
        cursor = mydb.cursor(prepared = True)
        sql = 'DELETE FROM likes WHERE post_postID = ? AND who_liked = ?'
        values = (post_id, session['id'])
        cursor.execute(sql, values)
        mydb.commit()

        return redirect(
            url_for('posts')
        )

    one_like = Likes(None, user_id, post_id, session['id'])
    one_like.add_like()

    mydb.commit()

    return redirect(
        url_for('posts')
    )


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


app.run(debug = True)
