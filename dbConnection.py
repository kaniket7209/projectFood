import mysql.connector
import logging

def dbConnection():
    mydb = mysql.connector.connect(
    host="localhost", # replace with "Database url for deployment"
    port = 3306,
    user="root",
    password= "",
    database = "Cloudbelly"  

    )
    # cur = mydb.cursor()
    # cur.execute("CREATE DATABASE IF NOT EXISTS Cloudbelly ")
    # mydb.commit()
    # cur.execute("USE Cloudbelly;")
    # mydb.commit()
    # cur.close()
    return mydb

def createTableRegisterInfo():
    try:
        mydb = dbConnection()
        mydb.reconnect()
        cur = mydb.cursor()
        query = """CREATE TABLE IF not exists registered_users_info(mobile_no VARCHAR(13),  email_id VARCHAR(100),password VARCHAR(500), PRIMARY KEY(mobile_no));"""
        cur.execute(query)
        mydb.commit()
        cur.close()
        return True
    except Exception as e:
        logging.warning(e)
        return

def createTableUserPersonaalDetails():
    try:
        mydb = dbConnection()
        mydb.reconnect()
        cur = mydb.cursor()
        query = """CREATE TABLE IF not exists users_personal_info( user_id INT NOT NULL AUTO_INCREMENT ,storeName VARCHAR(200),  tagline VARCHAR(500),category VARCHAR(100),phone_no VARCHAR(13),whatsapp_no VARCHAR(13),address VARCHAR(100),store_timing_start VARCHAR(100),store_timing_end VARCHAR(100), PRIMARY KEY(user_id));"""
        cur.execute(query)
        mydb.commit()
        cur.close()
        return True
    except Exception as e:
        logging.warning(e)
        return
        
    
    
    