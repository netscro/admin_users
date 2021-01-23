import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin, RoleMixin


app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'admin_users.db')
db_uri = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SECRET_KEY'] = 'dfgefge2354234fsdfwefwefsdf23432wefwd'
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())


@app.route('/')
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
