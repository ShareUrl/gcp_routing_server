import logging
import os
import MySQLdb
import string
import random

from flask import Flask, render_template, request, json

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db=CLOUDSQL_DATABASE)

    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=CLOUDSQL_DATABASE)

    return db


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/<url>")
def navigate(url):
    return render_template('navigate.html')


@app.route("/url/<hashUrl>")
def sendUrl(hashUrl):
    # print hashUrl
    query = "select tags from book where value='{0}'"
    # print query.format(hashUrl)
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute(query.format(hashUrl))
    # fetch all of the rows from the query
    data = cursor.fetchall()
    # print the rows
    # print data
    myData = ""
    for row in data:
        # log data
        # print row[0]
        myData = str(row[0])
    if len(myData) > 0:
        return myData
    else:
        return "not cool"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route("/createUrl", methods=['POST'])
def createUrl():
    db = connect_to_cloudsql()
    cursor = db.cursor()
    data = request.get_data()
    val = id_generator()
    query = "INSERT INTO book(value,tags) VALUES('{0}',{1});"
    #print (val, data)
    cursor.execute(query.format(val,data))
    happn = cursor.fetchall()
    if len(happn) is 0:
        db.commit()
        return val
    else:
        return json.dumps({'error': str(data[0])})


@app.route("/datas")
def datas():
    db = connect_to_cloudsql()
    cursor = db.cursor()

    cursor.execute('SELECT * from book')
    str1 = ""
    for r in cursor.fetchall():
        str1 = str1 + format(r)
    return str1

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
