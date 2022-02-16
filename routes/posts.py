from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
from classes.user import User
import mysql.connector
from classes.post import Post

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'drustvena'
)

posts_app = Blueprint('posts', __name__, static_folder="static", template_folder="templates")

@posts_app.route('/posts')
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


    ###################
    #Prostor za rad
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT comment.commentID, comment.content, comment.post_postID, user.firstName, user.last_name, user.username, user.profile_image FROM comment INNER JOIN user ON comment.user_uderID = user.uderID;'
    cursor.execute(sql)
    comment_user_join = cursor.fetchall()

    g = len(comment_user_join)
    for i in range(g):
        comment_user_join[i] = dekodiraj(comment_user_join[i])

    #comment_user_join izgleda ovako:
    #[['commentID','commentContent','postID','firstname','lastname','username','profilePicture']
    ###############

    #Moramo da znamo ko je sve komentarisao post, tj svaki post
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * from comment;'
    cursor.execute(sql)
    comments = cursor.fetchall()

    v = len(comments)
    for i in range(v):
        comments[i] = dekodiraj(comments[i])

    all_comments_posts = [] #Ovo je ko je sve komentarisao jedan post...

    for i in range(len(posts_res)):
        one_post = []
        for j in range(len(comment_user_join)):
            one_comment = []
            if posts_res[i][0] == comment_user_join[j][2]:
                one_comment.append(comment_user_join[j][1])  #Comment content
                one_comment.append(comment_user_join[j][3])  #Firstname
                one_comment.append(comment_user_join[j][4])  #Lastname
                one_comment.append(comment_user_join[j][5])  #username
                one_comment.append(comment_user_join[j][6])  #Profile picture
                one_post.append(one_comment)
        one_post.append(len(one_post)) #Da znao koliko post ima komntara
        all_comments_posts.append(one_post)
    

    # return str(all_comments_posts)


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

    #return str(all_comments_posts)

    return render_template(
        'posts.html',
        posts = posts,
        users = users,
        m = m,
        join_res = join_res,
        likes_join = likes_join,
        all_posts = all_posts,
        all_comments_posts = all_comments_posts
    )

def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data