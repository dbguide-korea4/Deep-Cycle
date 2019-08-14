from flask import Flask, render_template, request, redirect, session, url_for
from models import db, UserTable
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///deep_cycle.db'
)
app.secret_key = 'anything'

#db = SQLAlchemy(app)
db.init_app(app)
admin = Admin(app, name="UserTable View")

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
        #print(userid)
        try:
            data = UserTable.query.filter_by(id=userid, pw=userpw).first()
            if data is not None:
                #print(data)
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
        new_user = UserTable(id = request.form['id'], pw = request.form['password'], name=request.form['user_name'], email=request.form['user_email'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html')
    return render_template('register.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
