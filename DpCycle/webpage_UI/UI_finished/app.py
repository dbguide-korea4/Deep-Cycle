from flask import Flask, render_template
from flask_dropzone import Dropzone
#

#
app = Flask(__name__)

dropzone = Dropzone(app)

@app.route('/')
def hello_world():
    return render_template('index.html')
#
@app.route('/file-upload', methods=['GET', 'POST'])
def file_upload():
    return 'test'


if __name__ == '__main__':
    app.run()