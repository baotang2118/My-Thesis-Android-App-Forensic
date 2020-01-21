import mysql.connector
from androguard.cli import androlyze_main
from androguard.core.androconf import *
from androguard.misc import *


def main():
    # create database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=""
        )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS thesis_1920_datasheet_databases")
    mycursor.close()
    mydb.close()

    # create table
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_datasheet_databases"
        )

    mycursor = mydb.cursor()

    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS datasheet (apk_id INTEGER PRIMARY KEY AUTO_INCREMENT, package_name text, dir text)")
    mycursor.close()
    mydb.close()

if __name__ == "__main__":
	main()