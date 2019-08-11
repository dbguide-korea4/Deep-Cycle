import os

from models import db, UserTable
from flask import Flask, render_template, request, redirect, redirect, session, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 작업하고 있는 절대경로.

app = Flask(__name__)

app.config.update(  # app.config : 설정. update는 기존 설정을 업데이트.
    SQLALCHEMY_DATABASE_URI='sqlite:///deep_cycle.db',
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),  # 파일을 업로드 했을 때 어디로 저장?
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_DEFAULT_MESSAGE='Click or Drop your Image'
)
app.secret_key = 'anything'
#db = SQLAlchemy(app)

db.init_app(app)
admin = Admin(app, name="UserTable View")

dropzone = Dropzone(app)


class MyModelView(ModelView):
    can_delete = True
    can_view_details = True


admin.add_view(MyModelView(UserTable, db.session))


@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            return render_template('index.html')
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['id']
        userpw = request.form['password']
        # print(userid)
        try:
            data = UserTable.query.filter_by(id=userid, pw=userpw).first()
            if data is not None:
                # print(data)
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template("login_fail.html")
        except:
            return render_template("login_fail.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = UserTable(id=request.form['id'], pw=request.form['password'],
                             name=request.form['user_name'], email=request.form['user_email'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html')
    return render_template('register.html')


@app.route('/uploads', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if not os.path.isdir(app.config['UPLOADED_PATH']):
            os.makedirs(app.config['UPLOADED_PATH'])

        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')


@app.route('/completed')
def completed():
    return '<h1>The Redirected Page</h1><p>Upload completed.</p>'


if __name__ == '__main__':
    app.run(debug=True)
