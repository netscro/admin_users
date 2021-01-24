from flask import Blueprint
from flask_admin import Admin


adm = Blueprint('adm', __name__, template_folder='templates')
admin = Admin()


@adm.route('/home')
def admin():
    return '<h1>Second app</h1>'
