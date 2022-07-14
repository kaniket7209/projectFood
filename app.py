from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/sign_in', methods = ["POST","GET"])
def sign_in():
    if request.method == "POST":
        print("Success",request.form)
        phone_no = request.form['phone_no']
        otp = request.form['enter_otp']
        password = request.form['password']
        
        print(phone_no,otp,password)
    return "Sign IN Success"
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)