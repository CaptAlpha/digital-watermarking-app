from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask import jsonify
import pandas as pd
import os


application = Flask(__name__)
filepath=""
orig_name=""
@application.route('/', methods=['GET', 'POST'])
def index():

    global orig_name
    filepath = "NOT FOUND"
    df = pd.DataFrame()
    accuracy=0
    final=''
    Keymax=''
    if request.method == 'POST':
        file = request.files['cover']
        orig_name=file.filename
       
        if not os.path.isdir('static/assets'):
            os.mkdir('static/assets')

        if os.path.isfile("static/assets/cover.jpg"):
            os.remove("static/assets/cover.jpg") 
        
        filepath = os.path.join('static/assets', file.filename)
        newName = "static/assets/cover.jpg"
        
        file.save(filepath)
        fp = os.rename(filepath, newName)
        
        
            
        return redirect(url_for('task'))


    return render_template('index.html', filepath=filepath, df = df)

@application.route('/task', methods=['GET', 'POST'])
def task():

    return render_template('task.html')

if __name__ == '__main__':
    application.run(debug=True)