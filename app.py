from flask import Flask, render_template,request,redirect,url_for,session
import logging
app = Flask(__name__)

@app.route('/')
def home():    
    return render_template('home.html')

@app.route('/sign_up', methods = ["POST","GET"])
def sign_up():

    if request.method == "POST":
        from functions import otpgen
   
        phone_no = request.form['phone_no']
        email = request.form['enter_email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        print(phone_no,email,password)
        if password != confirmPassword:
            return redirect(url_for('home'))
        
        
        otp = otpgen()
        # implement feature to send otp to mobile number here
        session['user_phone_no'] = phone_no
        session['otp'] = otp
        print(otp)
        return redirect(url_for('verification'))
        
        
      
    return "Sign IN Success"

@app.route('/send_otp')
def send_otp():
    
    return "True"

@app.route('/verification',methods = ["POST","GET"] )
def verification():
    if request.method == "POST":
        otpEntered = request.form['otp']
        if otpEntered == session['otp']:
            return redirect(url_for('sign_up_success'))
        else:
            logging.warning("OTP Entered is incorrect . Please try Again")
            return redirect(url_for('verification'))
    return render_template('verification.html')

@app.route('/sign_up_success')
def sign_up_success():
    return render_template('sign_up_success.html')

if __name__ == "__main__":
    app.secret_key = "232422"
  
    app.run(debug=True,host="0.0.0.0",port=8000)