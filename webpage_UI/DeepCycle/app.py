import os

from flask import Flask, render_template,request, redirect
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__)) #현재 작업하고 있는 절대경로.

app = Flask(__name__)

app.config.update( # app.config : 설정. update는 기존 설정을 업데이트.
    UPLOADED_PATH=os.path.join(basedir, 'uploads'), # 파일을 업로드 했을 때 어디로 저장?
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
    DROPZONE_UPLOAD_ON_CLICK=True
)

dropzone = Dropzone(app)

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

    return render_template('index.html')

@app.route('/b')
def red():
    return redirect('/')

@app.route('/completed')
def completed():
    return '<h1>The Redirected Page</h1><p>Upload completed.</p>'

if __name__ == '__main__':
    app.run(debug=True)
