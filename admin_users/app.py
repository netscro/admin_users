import os

from flask import Flask, render_template, url_for, redirect, request
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore,\
    Security, current_user
from flask_migrate import Migrate
# second admin
from adm import adm


app = Flask(__name__)
app.register_blueprint(adm, url_prefix='/adm')

# path to admin database
db_path = os.path.join(os.path.dirname(__file__), 'admin_users.db')
db_uri = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SECRET_KEY'] = 'dfgefge2354234fsdfwefwefsdf23432wefwd'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask-Security-Too
app.config['SECURITY_PASSWORD_SALT'] = 'sdafsDF345345ERGARDG34543'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % (self.username)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % (self.name)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Security Admin
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


# users and links in admin
admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
admin.add_link(MenuLink(name='Admin-2', category='', url="/adm/admin"))


@app.route('/')
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
