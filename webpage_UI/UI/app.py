from flask import Flask, render_template
# from flask_dropzone import Dropzone

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()