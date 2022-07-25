
from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging
from werkzeug.utils import secure_filename
import os     
from functools import wraps
import json
import requests
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

# ----DB CHECK


def checkDbConnection():
    from dbConnection import dbConnection
    mydb = dbConnection()
    if mydb:
        print("Connected to db")
        return mydb
    else:
        logging.warning("Please connect database first")
        return


mydb = checkDbConnection()

# ---------

# middle ware


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Nice try, Tricks don\'t work, bud!! Please Login :)')
            return redirect(url_for('sign_in'))
    return wrap


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sign_up', methods=["POST", "GET"])
def sign_up():

    if request.method == "POST":
        from functions import otpgen

        phone_no = request.form['phone_no']
        email = request.form['enter_email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        print(phone_no, email, password)
        if password != confirmPassword:
            return redirect(url_for('home'))
        from dbConnection import createTableRegisterInfo
        createTableRegisterInfo()
        
        mydb.reconnect()
        cur = mydb.cursor()
        cur.execute(
            "SELECT COUNT(mobile_no) FROM registered_users_info WHERE mobile_no = %s", [phone_no])
        count = cur.fetchall()[0][0]
        print(count, "--------49")
        if count >= 1:
            print("when trying to use same mobile no for multiple accounts")
            session['user_phone_no'] = "0"
            return redirect(url_for('sign_up'))

        # hashing password

        hashPass = pbkdf2_sha256.hash(password)
        print(hashPass, "--------45")

        otp = otpgen()
        # implement feature to use api service to send  otp to mobile number here
        try:
            res = requests.get(
                "http://localhost:8000/sendOTP?number={}&otp={}".format(phone_no, otp))
            print(res.status_code)
        except Exception as e:
            print(e)

        # ex aml ( sendOTP(mobile_no)) where mobile_no is a payload sendOTP is an API (route > send_otp)
        session['user_phone_no'] = phone_no
        session['otp'] = otp
        session['password'] = hashPass
        session['email'] = email
        print(otp)

        return redirect(url_for('verification'))

    return render_template('home.html')


@app.route('/send_otp_again')
def send_otp_again():
    from functions import otpgen
    otp = otpgen()
    res = requests.get(
        "http://localhost:8000/sendOTP?number={}&otp={}".format(session['user_phone_no'], otp))
    print(res.status_code)
    session['otp'] = otp
    return redirect(url_for('verification'))


@app.route('/verification', methods=["POST", "GET"])
def verification():
    if request.method == "POST":
        try:
            otpEntered = request.form['otp']
            if otpEntered == session['otp']:

                # storing data in db if verified
                from dbConnection import createTableRegisterInfo
                if not createTableRegisterInfo():
                    return

                # check data present in registered
                mydb.reconnect()
                cur = mydb.cursor()
                cur.execute("SELECT COUNT(mobile_no) FROM registered_users_info WHERE mobile_no = %s", [
                            session['user_phone_no']])
                count = cur.fetchall()[0][0]
                # print(count,"--")
                if count >= 1:  # for registered user  login verification
                    return redirect(url_for('personal_details'))
                    # redirect to store

                elif createTableRegisterInfo() == True and count == 0:  # if table is created
                    mydb.reconnect()
                    cur = mydb.cursor()
                    print(session['password'], session['user_phone_no'])
                    insertQuery = """INSERT into registered_users_info (mobile_no, email_id, password) VALUES(%s, %s, %s)"""
                    val = (session['user_phone_no'],
                           session['email'], session['password'])
                    cur.execute(insertQuery, val)
                    mydb.commit()
                    cur.close()

                    return redirect(url_for('sign_in'))
            else:
                logging.warning("OTP Entered is incorrect . Please try Again")
                return redirect(url_for('verification'))
        except Exception as e:
            print(e)
    return render_template('verification.html')


@app.route('/sign_in', methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        try:
            phone_no = request.form['phone_no']
            password = request.form['password']
            session['user_phone_no'] = phone_no
            if not password:
                return redirect(url_for('send_otp_again'))

            # fetch data from db to validate
            mydb.reconnect()
            cur = mydb.cursor()
            cur.execute(
                "SELECT mobile_no, password FROM registered_users_info WHERE mobile_no = %s", [phone_no])
            result = cur.fetchall()
            phoneNumber = result[0][0]
            hashPassword = result[0][1]
            print(phoneNumber, password)
            cur.close()
            if phone_no == phoneNumber and pbkdf2_sha256.verify(password, hashPassword):
                session['logged_in'] = True
                session['password'] = "NIce Try Boi..."
                session['otp'] = "Again Nice try Boi"
                return redirect(url_for('personal_details'))

            else:
                return redirect(url_for('sign_in'))
        except Exception as e:
            print(e)

    return render_template('sign_in.html')


# --Store Setup----
categoryJson = {
    1: "Restaurant",
    2: "Cloud Kitchen",
    3: "Stall",
    4: "Content Creato",
    5: "Home Kitchen",
}


@app.route('/personal_details', methods=["POST", "GET"])
@is_logged_in
def personal_details():
    if request.method == "POST":
        # required fields
        tagline = request.form['tagline']
        saveImageDirPath = os.path.join(os.getcwd(), 'static/Media')
        image = request.files['storeLogo']
        if image:
            print(image)
            image.save(os.path.join(saveImageDirPath,
                       secure_filename(image.filename)))

        personal_details_json = {
            "storeName": request.form['storeName'],
            "tagline" : request.form['tagline'],
            "category": request.form['category'],
            "phone_no": request.form['phone_no'],
            "whatsapp_no": request.form['whatsapp_no'],
            "address": request.form['address'],
            "store_timing": request.form['store_timing_start'],
            "store_timing_end": request.form['store_timing_end'],
        }
        print(personal_details_json)
    return render_template('personal_details.html')


@app.route("/logout/")
@is_logged_in
def logout():
    session["logged_in"] = None
    session['user_phone_no'] = None
    flash("Successfully Logged out")
    return redirect(url_for('sign_in'))


if __name__ == "__main__":
    app.secret_key = "232422"

    app.run(debug=True, host="0.0.0.0", port=5000)
