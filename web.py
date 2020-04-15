from flask import Flask, render_template, make_response, session
from counter import Counter
import threading


app = Flask(__name__)


@app.route('/users/')
def users_page():
    counter = Counter('count_data', 'users')
    if session == {}:
        session['id'] = counter.next_user_id()
    if session['id'] != counter.count_data['last_id']:
        counter.count_data['last_id'] = session['id']
    counter.make_count()
    counter.upload_metadata('users', session['id'])
    return render_template('index.html', **counter.count_data)


@app.route('/main_page/')
def main_page():
    counter = Counter('count_data', 'main_page')
    if session == {}:
        session['id'] = counter.next_user_id()
    if session['id'] != counter.count_data['last_id']:
        counter.count_data['last_id'] = session['id']
    counter.make_count()
    counter.upload_metadata('main_page', session['id'])
    return render_template('index.html', **counter.count_data)


@app.route('/settings/')
def init_page():
    counter = Counter('count_data', 'settings')
    if session == {}:
        session['id'] = counter.next_user_id()
    if session['id'] != counter.count_data['last_id']:
        counter.count_data['last_id'] = session['id']
    counter.make_count()
    counter.upload_metadata('main_page', session['id'])
    return render_template('index.html', **counter.count_data)


if __name__ == '__main__':
    app.secret_key =\
        b'\xcabb\x3f\xbfd\x146\x9a1\x1d4\x1a\x23\xa2\x11re\x19a21\xf19\xf1\xeaf1'
    app.run()
