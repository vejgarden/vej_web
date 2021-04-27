from flask import Flask, render_template
import os
import glob

IMG_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route('/')
@app.route('/index')
def show_index():
    files=glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.jpg'))
    files.sort() #last one is the latest
    return render_template("index.html", user_image = files[-1])
