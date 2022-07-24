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
        
    
    
    