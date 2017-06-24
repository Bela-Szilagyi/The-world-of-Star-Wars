from flask import Flask, render_template, request, redirect, session, url_for, \
                  escape, make_response, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import data_manager
import os
import requests

app = Flask(__name__)


app.secret_key = os.urandom(24)


username = ''


@app.route('/')
def index():
    if 'username' in session:
        global username
    return render_template('index.html', username=username)


@app.route('/register/', methods=['GET'])
def get_register():
    return render_template('register.html', username='')


@app.route('/register/', methods=['POST'])
def post_register():
    username_to_register = request.form['username']
    text = 'SELECT username \
            FROM swuser\
            WHERE username = %s;'
    data = (username_to_register, )
    result = data_manager.handle_database(text, data)
    if result['result'] == 'success':
        if result['row_count'] == 0:
            if request.form['password'] != request.form['confirm-password']:
                flash('Password confirmation falied. Please re-enter password!')
                return render_template('register.html', username=username_to_register)
            else:
                password = generate_password_hash(request.form['password'])
                text = "INSERT INTO swuser(username, password) \
                        VALUES(%s, %s)"
                data = (username_to_register, password)
                result = data_manager.handle_database(text, data)
                if result['result'] == 'success':
                    text = "SELECT username \
                            FROM swuser\
                            WHERE username = %s"
                    data = (username_to_register, )
                    result = data_manager.handle_database(text, data)
                    if result['result'] == 'success':
                        info = True
                        return render_template('register.html', info=info)
                    else:
                        return render_template('error.html', error=result['result'])
                else:
                    return render_template('error.html', error=result['result'])
        else:
            flash('Username already in database! Choose another username')
            return redirect(url_for('get_register'))
    else:
        return render_template('error.html', error=result['result'])


@app.route('/login/', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def post_login():
    username_to_login = request.form['username']
    text = "SELECT username \
             FROM swuser\
             WHERE username = %s"
    data = (username_to_login, )
    result = data_manager.handle_database(text, data)
    if result['result'] == 'success':
        if result['row_count'] != 0:
            password = request.form['password']
            text = "SELECT password \
                    FROM swuser \
                    WHERE username = %s"
            data = (username_to_login, )
            result = data_manager.handle_database(text, data)
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
                    flash('Authentification failed. Try to login again!')
                    return redirect(url_for('get_login'))
        else:
            flash('Username not registered. Try to login again!')
            return redirect(url_for('get_login'))
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
    text = "SELECT id \
            FROM swuser\
            WHERE username = %s"
    data = (username, )
    result = data_manager.handle_database(text, data)
    if result['result'] != 'success':
        return render_template('error.html', error='Error handling your vote. Try to vote again!')
    else:
        swuser_id = result['rows'][0][0]
        text = "INSERT INTO planetvotes(planet_id, swuser_id, submission_time) \
                    VALUES (%s, %s, %s)"
        data = (voted_planet_id, swuser_id, str(datetime.now())[:-7])
        result = data_manager.handle_database(text, data)
        if result['result'] != 'success':
            return render_template('error.html', error='Error handling your vote. Try to vote again!')
        else:
            return redirect(url_for('index'))


@app.route('/statistics/', methods=['POST'])
def statistics():
    text = "SELECT planet_id, count(planet_id) \
            FROM planetvotes \
            GROUP BY planet_id \
            ORDER BY planet_id"
    data = None
    result = data_manager.handle_database(text, data)
    if result['result'] == 'success':
        statistics = []
        for row in result['rows']:
            planet_name = get_planet_name(row[0])
            statistics.append([planet_name, row[1]])
        statistics.sort()
        json_statistics = jsonify(statistics)
        return json_statistics
    else:
        return render_template('error.html', error='Error handling statistics. Try again!')


def get_planet_name(planet_id):
    response = requests.get('http://swapi.co/api/planets/' + str(planet_id))
    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        return render_template('error.html', error='Error handling statistics. Try again!')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e), 404


@app.errorhandler(500)
def internal_server(e):
    return render_template('error.html', error=e), 500


if __name__ == '__main__':
    app.run(debug=True)
