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
from dct_watermark import DCT_Watermark
from dwt_watermark import DWT_Watermark
import cv2

def black_box():
    print("black")

application = Flask(__name__)
filepath=""
orig_name=""
model = black_box()
task_type = black_box()

"""  _   _                        ____             _       
 | | | | ___  _ __ ___   ___  |  _ \ ___  _   _| |_ ___ 
 | |_| |/ _ \| '_ ` _ \ / _ \ | |_) / _ \| | | | __/ _ \
 |  _  | (_) | | | | | |  __/ |  _ < (_) | |_| | ||  __/
 |_| |_|\___/|_| |_| |_|\___| |_| \_\___/ \__,_|\__\___|
                                                        """
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
        file2 = request.files['watermark']

       
        if not os.path.isdir('static/assets'):
            os.mkdir('static/assets')

        if os.path.isfile("static/assets/cover.jpg"):
            os.remove("static/assets/cover.jpg") 
        
        if os.path.isfile("static/assets/watermark.jpg"):
            os.remove("static/assets/watermark.jpg") 

        filepath = os.path.join('static/assets', file.filename)
        filepath2 = os.path.join('static/assets', file2.filename)
        newName = "static/assets/cover.jpg"
        newName2 = "static/assets/watermark.jpg"

        type=request.form['type']
        if type == 'DCT':
            model = DCT_Watermark()
        elif type == 'DWT':
            model = DWT_Watermark()
        

        file.save(filepath)
        file2.save(filepath2)
        fp = os.rename(filepath, newName)
        fp2 = os.rename(filepath2, newName2)
        
        
            
        return redirect(url_for('task'))


    return render_template('index.html', filepath=filepath, df = df)

"""
  _____         _      ____             _       
 |_   _|_ _ ___| | __ |  _ \ ___  _   _| |_ ___ 
   | |/ _` / __| |/ / | |_) / _ \| | | | __/ _ \
   | | (_| \__ \   <  |  _ < (_) | |_| | ||  __/
   |_|\__,_|___/_|\_\ |_| \_\___/ \__,_|\__\___|
                                                
"""
emb_img = black_box()
@application.route('/task', methods=['GET', 'POST'])
def task():
    if os.path.isfile("static/assets/cover.jpg") and os.path.isfile("static/assets/watermark.jpg"):
        img = cv2.imread("static/cover.jpg")
        wm = cv2.imread("static/watermark.jpg", cv2.IMREAD_GRAYSCALE)
    else:
        return redirect(url_for('error_page'))
    filepath = "NOT FOUND"
    global orig_name
    if request.method == 'POST':
        task=request.form['task']
        if task == 'DCT':
            model = DCT_Watermark()
        elif task == 'DWT':
            model = DWT_Watermark() 

        if os.path.isfile("static/assets/embedded.jpg"):
            os.remove("static/assets/embedded.jpg") 

       
        
        
    return render_template('task.html')

if __name__ == '__main__':
    application.run(debug=True)