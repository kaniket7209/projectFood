
from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging

from werkzeug.utils import secure_filename
import os
from functools import wraps
import json
import requests

UPLOAD_FOLDER = os.path.join('images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# middle ware
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Nice try, Tricks don\'t work, bud!! Please Login :)')
            return redirect(url_for('login'))
    return wrap

@app.route('/register',methods = ['POST','GET'])
def register():
    from authentication.base import saveData
    
    if not (request.method == 'POST'):
        return {
            "data":{},
            "msg":"GET REQUEST NOT ALLOWED",
            "code":404,
            "error":True
        }
    data = request.get_json()

    res = saveData(data)
    
    return res
    # email, password, phone_number
    
    return "Register"

@app.route('/login',methods = ['POST','GET'])
def login():
    if not (request.method == 'POST'):
        return {
            "data":{},
            "msg":"GET REQUEST NOT ALLOWED",
            "code":404,
            "error":True
        }
    try:
        data = request.get_json()
        
        from authentication.base import validate
        method = request.args['auth']
        res = {}
        if method == 'number':
            res =validate(data,'number')
        elif method == 'email':
            res = validate(data,'email')
        if res['code'] == 200:
            session['logged_in'] = True
        return res
            
    except Exception as e:
        return {
            "data":{},
            "msg":str(e),
            "code":404,
            "error":True
        }

@app.route('/menu-update',methods=['POST','GET'])
def menuExtract():
    import os
    if request.method == 'POST':
        from werkzeug.utils import secure_filename
        # ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        uploaded_img = request.files['uploaded-file']
        img_filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # session['uploaded_img_file_path'] = os.path.join('images', img_filename)
    
    return  render_template('cropper.html')

@app.route('/store-setup/<function>',methods=['POST','GET'])
def storeSetup(function):
    import os
    
    if request.method == 'GET':
        return {
            "code":404,
            "msg":"Only POST req allowed",
            "error":True,
            "data":{}
        }
        
    if request.method == 'POST':
        from store.base import base
        
        data = request.get_json()
        return base(function,data)
        
    return {
            "code":500,
            "msg":"Unknown Error",
            "error":True,
            "data":{}
        }
    


if __name__ == "__main__":
    app.secret_key = "xjhasvcjhcloudbellyjhsbcahb"

    app.run(debug=True, host="0.0.0.0", port=5000)
