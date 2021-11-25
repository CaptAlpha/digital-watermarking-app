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
from attack import Attack
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
            session['model'] = 1
        elif type == 'DWT':
            session['model'] = 2
        
        print(model)

        file.save(filepath)
        file2.save(filepath2)
        fp = os.rename(filepath, newName)
        fp2 = os.rename(filepath2, newName2)
        
        
            
        return redirect(url_for('task'))


    return render_template('index.html', filepath=filepath, model=model)

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
        img = cv2.imread("static/assets/cover.jpg")
        wm = cv2.imread("static/assets/watermark.jpg", cv2.IMREAD_GRAYSCALE)
    else:
        return redirect(url_for('error_page'))
    filepath = "NOT FOUND"
    global orig_name
    model = session.get('model', None)
    if request.method == 'POST':
        task=request.form['task']
        if task == 'embedding':
            if model == 1:
                model = DCT_Watermark()
            elif model == 2:
                model = DWT_Watermark()
            if task == 'embedding':
                emb_img = model.embed(img, wm)
            elif task == 'extracting':
                emb_img = model.embed(img, wm)
            model = session.get('model', None)
            
            if os.path.isfile("static/assets/embedded.jpg"):
                os.remove("static/assets/embedded.jpg") 

            
            
            cv2.imwrite("static/assets/embedded.jpg", emb_img)
            print("Embedded to {}".format("static/assets/embedded.jpg"))

            return redirect(url_for('attack'))
        
        elif task == 'extracting':

            return redirect(url_for('extract'))
        
    return render_template('task.html')

""" 
    _   _   _             _      ____             _       
    / \ | |_| |_ __ _  ___| | __ |  _ \ ___  _   _| |_ ___ 
   / _ \| __| __/ _` |/ __| |/ / | |_) / _ \| | | | __/ _ \
  / ___ \ |_| || (_| | (__|   <  |  _ < (_) | |_| | ||  __/
 /_/   \_\__|\__\__,_|\___|_|\_\ |_| \_\___/ \__,_|\__\___|
                                                           """
att_img = black_box()
@application.route('/attack', methods=['GET', 'POST'])
def attack():
     
    if os.path.isfile("static/assets/cover.jpg") and os.path.isfile("static/assets/watermark.jpg"):
        img = cv2.imread("static/assets/cover.jpg")
        wm = cv2.imread("static/assets/watermark.jpg", cv2.IMREAD_GRAYSCALE)
        em = cv2.imread("static/assets/embedded.jpg")
    else:
        return redirect(url_for('error_page'))
    if request.method == 'POST':
        filepath = "NOT FOUND"
        global orig_name
        model = session.get('model', None)
        attack =request.form['attack']
        if os.path.isfile("static/assets/attacked.jpg"):
            os.remove("static/assets/attacked.jpg") 
        if(attack == 'blur'):
            att_img = Attack.blur(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'no-attack'):
            cv2.imwrite("static/assets/attacked.jpg", img)
        elif(attack == 'rotate180'):
            att_img = Attack.rotate180(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'rotate90'):
            att_img = Attack.rotate90(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'chop5'):
            att_img = Attack.chop5(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'chop10'):
            att_img = Attack.chop10(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'chop30'):
            att_img = Attack.chop30(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'randline'):
            att_img = Attack.randline(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'cover'):
            att_img = Attack.cover(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'brighter10'):
            att_img = Attack.brighter10(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'darker10'):
            att_img = Attack.darker10(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'saltnoise'):
            att_img = Attack.saltnoise(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'largersize'):
            att_img = Attack.largersize(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)
        elif(attack == 'smallersize'):
            att_img = Attack.smallersize(em)
            cv2.imwrite("static/assets/attacked.jpg", att_img)


        print(attack)
        return redirect(url_for('extract'))
        
        if os.path.isfile("static/assets/attacked.jpg"):
                os.remove("static/assets/attacked.jpg")

    return render_template('attack.html')


"""
  _____      _                  _     ____             _       
 | ____|_  _| |_ _ __ __ _  ___| |_  |  _ \ ___  _   _| |_ ___ 
 |  _| \ \/ / __| '__/ _` |/ __| __| | |_) / _ \| | | | __/ _ \
 | |___ >  <| |_| | | (_| | (__| |_  |  _ < (_) | |_| | ||  __/
 |_____/_/\_\\__|_|  \__,_|\___|\__| |_| \_\___/ \__,_|\__\___|
                                                               
"""
signature = black_box()
@application.route('/extract',methods=['GET', 'POST'])
def extract():
    if os.path.isfile("static/assets/cover.jpg") and os.path.isfile("static/assets/watermark.jpg"):
        img = cv2.imread("static/assets/cover.jpg")
        wm = cv2.imread("static/assets/watermark.jpg", cv2.IMREAD_GRAYSCALE)
        em = cv2.imread("static/assets/embedded.jpg")
        at = cv2.imread("static/assets/attacked.jpg")
    else:
        return redirect(url_for('error_page'))
    model = session.get('model', None)
    if request.method == 'POST':
        filepath = "NOT FOUND"
        global orig_name
       
        
        if os.path.isfile("static/assets/signature.jpg"):
            os.remove("static/assets/signature.jpg") 
        model = session.get('model', None)
        if model == 1:
            model = DCT_Watermark()
        elif model == 2:
            model = DWT_Watermark()

        task=request.form['task']
        if task == 'extract':
            signature = model.extract(img)




        elif model == 'attack':
            return redirect(url_for('attack'))
        
        


        
        
        cv2.imwrite("static/assets/signature.jpg", signature)
        print("Embedded to {}".format("static/assets/signature.jpg"))

        return redirect(url_for('signature'))
        if os.path.isfile("static/assets/signature.jpg"):
                os.remove("static/assets/signature.jpg")
    return render_template('extract.html')


"""
  ____  _                   _                    ____             _       
 / ___|(_) __ _ _ __   __ _| |_ _   _ _ __ ___  |  _ \ ___  _   _| |_ ___ 
 \___ \| |/ _` | '_ \ / _` | __| | | | '__/ _ \ | |_) / _ \| | | | __/ _ \
  ___) | | (_| | | | | (_| | |_| |_| | | |  __/ |  _ < (_) | |_| | ||  __/
 |____/|_|\__, |_| |_|\__,_|\__|\__,_|_|  \___| |_| \_\___/ \__,_|\__\___|
          |___/                                                           
"""
@application.route('/signature', methods=['GET', 'POST'])
def signature():

    return render_template('signature.html')


                                                       
@application.route('/error_page', methods=['GET', 'POST'])
def error_page():
    
    return render_template('error_page.html')

if __name__ == '__main__':
    application.secret_key = 'super secret key'
    application.run(debug=True)