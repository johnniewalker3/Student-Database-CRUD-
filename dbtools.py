import mysql.connector

MYSQL = mysql.connector


def open_connection():
    try:
        return MYSQL.connect(
            host="localhost",
            user="pyuser",
            password="pwd1234",
            database="pyuniversity"
        )
    except MYSQL.Error as e:
        print(e)


def alter_at_table(connection, query):
    try:
        mycursor = connection.cursor()
        mycursor.execute(query)
        mycursor.close()
    except MYSQL.Error as e:
        print(e)


def query_full_results(connection, query):
    try:
        mycursor = connection.cursor(dictionary=True)
        mycursor.execute(query)
        rows = mycursor.fetchall()
        mycursor.close()
        return rows
    except MYSQL.Error as e:
        print(e)


def query_one_result(connection, query):
    try:
        mycursor = connection.cursor(dictionary=True, buffered=True)
        mycursor.execute(query)
        row = mycursor.fetchone()
        while row is not None:
            yield row
            row = mycursor.fetchone()
        mycursor.close()
    except MYSQL.Error as e:
        print(e)


def query_many_results(connection, query):
    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        rows = cursor.fetchmany(5)
        while rows:
            yield rows
            rows = cursor.fetchmany(5)
        cursor.close()
    except MYSQL.Error as e:
        print(e)


def insert_at_table(connection, query, tuple_args):
    try:
        cursor = connection.cursor(dictionary=True)
        if tuple_args is None:
            cursor.execute(query)
        else:
            cursor.execute(query, tuple_args)
        lastrowid = None
        if cursor.lastrowid is not None:
            lastrowid = cursor.lastrowid
        cursor.close()
        return lastrowid
    except MYSQL.Error as e:
        print(e)


def delete_from_table(connection, query):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        cursor.close()
    except MYSQL.Error as e:
        print(e)


def update_table(connection, query):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        cursor.close()
    except MYSQL.Error as e:
        print(e)


def trigger_at_table(connection, query):
    try:
        mycursor = connection.cursor()
        mycursor.execute(query)
        mycursor.close()
    except MYSQL.Error as e:
        print(e)


def call_procedure(connection, proc_name, tuple_args):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc(proc_name, tuple_args)
        cursor.close()
    except MYSQL.Error as e:
        print(e)
