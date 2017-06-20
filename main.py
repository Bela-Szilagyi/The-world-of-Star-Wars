from flask import Flask, render_template, request, redirect, session, url_for, escape
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import data_manager

app = Flask(__name__)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


username = ''


@app.route('/')
def index():
    if 'username' in session:
        global username
    print('username ' + username)
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
        '''
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
        '''
    else:
        return render_template('error.html', error=result['result'])
    '''
    return 'username: ' + request.form['username'] + ' password: ' + request.form['password']
    '''


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
                    return redirect(url_for('index'))
                else:
                    return 'authentification failed: ' + str(password) + ' ' + str(password_from_database)
        else:
            return 'username not registered'
        '''
        return render_template('result.html',
                            title=title,
                            column_names=result['column_names'], rows=result['rows'], row_count=result['row_count'])
        '''
    else:
        return render_template('error.html', error=result['result'])
    '''
    return 'username: ' + request.form['username'] + ' password: ' + request.form['password']
    '''


@app.route('/logout/')
def logout():
    session.pop('username', None)
    global username
    username = ''
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
