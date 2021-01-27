import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

DB_NAME = 'attendance'
TABLES = {}

cnx = mysql.connector.connect(
    user='root',
    password='ayankhan',
    host='localhost',
)

cursor = cnx.cursor()


def create_database(cursor):
    try:
        cursor.execute(
            f"CREATE DATABASE {DB_NAME}"
        )
        print(f'Database {DB_NAME} created.')
    except:
        print("Failed to create database")
        exit(1)


try:
    cursor.execute(
        f"USE {DB_NAME}"
    )
    print(f"Database changed")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        create_database(cursor)

date = datetime.now().date().strftime("%d_%m_%Y")

TABLES[f'{date}'] = (
    f"CREATE TABLE `{date}`("
    f"`roll_no` int NOT NULL PRIMARY KEY,"
    f"`name` VARCHAR(50) NOT NULL,"
    f"`date_` date NOT NULL,"
    f"`time_` VARCHAR(15) NOT NULL"
    f")")

table_desc = TABLES[f'{date}']
try:
    print(f"creating table {date}")
    cursor.execute(table_desc)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print(f"{date} already exists")
    else:
        print(err.msg)
        exit(1)
else:
    print("OK")


def add_to_db(roll, name, date_, time_):
    try:
        add_person = f"INSERT INTO {date} (roll_no, name, date_, time_) VALUES (%s, %s, %s, %s)"
        data_person = (str(roll), name, date_, time_)
        cursor.execute(add_person, data_person)
        cnx.commit()
    except:
        print("already present!")
    else:
        print(f"{name} is present")
        print(cursor.rowcount, "record inserted")

# add_to_db(101, "ayan", datetime.now().date(), datetime.now().strftime("%Hh:%Mm:%Ss"))