import flask
import json
import mysql.connector

app = flask.Flask(__name__)


@app.route("/")
def hello_world():
    return "Coucou !"


@app.route("/widgets")
def widgets():
    database = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="password",
        database="inventory",
    )
    cursor = database.cursor()

    cursor.execute("SELECT * FROM widgets")

    row_headers = [column[0] for column in cursor.description]

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route("/initdb")
def init_db():
    database = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="password",
    )
    cursor = database.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    database = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="password",
        database="inventory",
    )
    cursor = database.cursor()

    cursor.execute("DROP DATABASE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return "init database"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
