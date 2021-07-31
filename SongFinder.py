from flask import Flask, render_template, request
import sqlalchemy
import sqlite3

app = Flask(__name__)


def beautify(info):
    if info is None:
        return 'No such song'

    name, composer, duration, price = info[1], info[5], info[6], info[8]

    return f'Name: {name}; Composer: {composer}; Duration: {duration}; Price: {price}'


@app.route('/', methods=["POST", "GET"])
def find():
    ready = False
    result = ""

    if request.method == "POST":
        name = request.form['song_name']
        result = beautify(sql_parse(name.title()))
        ready = True

    return render_template('finder.html', status=ready, res=result)


def sql_parse(song_name):
    print(song_name)

    conn = sqlite3.connect('chinook.db')
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM tracks
        WHERE Name = '""" + song_name + """'"""

    res = cursor.execute(query)

    return res.fetchone()


# sql_parse('"?"')

if __name__ == '__main__':
    app.run(debug=True)