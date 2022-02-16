from flask import Flask

#import BluePrints
from routes.login import login_app
from routes.register import register_app
from routes.edit import edit_app
from routes.create_post import create_post_app
from routes.add_comment import add_comment_app
from routes.add_like import add_like_app
from routes.logout import logout_app
from routes.posts import posts_app
from routes.home import home_app
from routes.profile import profile_app


#Register all BluePrints
app = Flask(__name__)
app.register_blueprint(login_app)
app.register_blueprint(register_app)
app.register_blueprint(edit_app)
app.register_blueprint(create_post_app)
app.register_blueprint(add_comment_app)
app.register_blueprint(add_like_app)
app.register_blueprint(logout_app)
app.register_blueprint(posts_app)
app.register_blueprint(home_app)
app.register_blueprint(profile_app)

app.config['SECRET_KEY'] = '27723dshhDJs!'

if __name__ == "__main__":
    app.run(debug = True)

