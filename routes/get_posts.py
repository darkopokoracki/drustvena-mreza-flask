from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, jsonify
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

get_posts_app = Blueprint('get_posts', __name__, static_folder="static", template_folder="templates")

@get_posts_app.route('/get_posts', methods=['POST'])
def get_posts():
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

    #Ovde ide rezultat komentara...
    cursor = mydb.cursor(prepared = True)
    sql = 'SELECT comment.commentID, comment.content, comment.post_postID, user.firstName, user.last_name, user.username, user.profile_image FROM comment INNER JOIN user ON comment.user_uderID = user.uderID;'
    cursor.execute(sql)
    comment_user_join = cursor.fetchall()

    g = len(comment_user_join)
    for i in range(g):
        comment_user_join[i] = dekodiraj(comment_user_join[i])

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

    # Treba da formirao jsonify
    posts = []
    for i in range(n):
        one_post_comments = []
        for comment in all_comments_posts[i][:-1]:
            one_post_comments.append(comment)

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

            'likes': likes_join[i][0], #Broj lajkova po postovima...
            'currentUser': [session['id'], session['firstname'], session['lastname'], session['picture'], session['username']],
            'whoLiked': all_posts[i],
            'isLiked': None,
            'comments': one_post_comments
        }

        posts.append(post)

    return jsonify(posts)


def dekodiraj(data):
    n = len(data)
    data = list(data)

    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()

    return data