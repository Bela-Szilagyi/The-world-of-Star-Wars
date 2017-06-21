from flask import Flask, render_template, request, redirect, session, url_for, \
                  escape, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import data_manager

app = Flask(__name__)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
'''
import os
os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
'''

username = ''


@app.route('/')
def index():
    if 'username' in session:
        global username
    return render_template('index.html', username=username)


@app.route('/register/', methods=['GET'])
def get_register():
    return render_template('register.html')


@app.route('/register/', methods=['POST'])
def post_register():
    username_to_register = request.form['username']
    query = "SELECT username \
             FROM swuser\
             WHERE username = '{}'".format(username_to_register)
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        if result['row_count'] == 0:
            password = generate_password_hash(request.form['password'])
            query = "INSERT INTO swuser(username, password) \
                     VALUES ('{}', '{}')".format(username_to_register, password)
            data_manager.handle_database(query)
            query = "SELECT username \
                    FROM swuser\
                    WHERE username = '{}'".format(username_to_register)
            result = data_manager.handle_database(query)
            if result['result'] == 'success':
                return str(result)
        else:
            return 'username already in database'
    else:
        return render_template('error.html', error=result['result'])


@app.route('/login/', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def post_login():
    username_to_login = request.form['username']
    query = "SELECT username \
             FROM swuser\
             WHERE username = '{}'".format(username_to_login)
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        if result['row_count'] != 0:
            password = request.form['password']
            query = "SELECT password \
                    FROM swuser \
                    WHERE username = '{}'".format(username_to_login)
            result = data_manager.handle_database(query)
            if result['result'] == 'success':
                password_from_database = result['rows'][0][0]
                if check_password_hash(password_from_database, password):
                    session['username'] = username_to_login
                    global username
                    username = username_to_login
                    redirection = redirect(url_for('index'))
                    response = make_response(redirection)
                    response.set_cookie("username", username)
                    return response
                else:
                    return 'authentification failed: ' + str(password) + ' ' + str(password_from_database)
        else:
            return 'username not registered'
    else:
        return render_template('error.html', error=result['result'])


@app.route('/logout/')
def logout():
    session.pop('username', None)
    global username
    username = ''
    redirection = redirect(url_for('index'))
    response = make_response(redirection)
    response.set_cookie("username", expires=0)
    return response


@app.route('/vote/', methods=['POST'])
def vote():
    vote = request.json['vote']
    voted_planet_id = json.loads(vote)['vote']
    username = json.loads(vote)['username']
    query = "SELECT id \
            FROM swuser\
            WHERE username = '{}'".format(username)
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        swuser_id = result['rows'][0][0]
    query = "INSERT INTO planetvotes(planet_id, swuser_id, submission_time) \
                VALUES ('{}', '{}', '{}')".format(voted_planet_id, swuser_id, str(datetime.now())[:-7])
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        return redirect(url_for('index'))


@app.route('/statistics/', methods=['POST'])
def statistics():
    query = "SELECT planet_id, count(planet_id) \
             FROM planetvotes \
             GROUP BY planet_id \
             ORDER BY planet_id"
    result = data_manager.handle_database(query)
    if result['result'] == 'success':
        statistics = {}
        for row in result['rows']:
            statistics[row[0]] = row[1]
        print(statistics)
        json_statistics = jsonify(statistics)
        print(json_statistics)
        return json_statistics


if __name__ == '__main__':
    app.run(debug=True)
