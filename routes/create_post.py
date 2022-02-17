from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, current_app
import os.path
from werkzeug.utils import secure_filename
from classes.post import Post

from database import mydb


create_post_app = Blueprint('create_post', __name__, static_folder="static", template_folder="templates")


@create_post_app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if len(session) == 0:
        return redirect(
            url_for('login.login')
        )

    if len(session) == 0:
        return redirect(
            url_for('login.login')
        )

    current_app.config['UPLOAD_FOLDER'] = 'static/images/posts'

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
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    else:
        return render_template(
            'create_post.html',
            extension_error = 'Ekstenzija nije dozvoljena!'
        )

    post = Post(None, title, content, image.filename, session['id'])
    post.add_post()
    mydb.commit()  #Moramo i ovde sacuvati da bi se relodovalo...

    return redirect(
        url_for('posts.posts')
    )