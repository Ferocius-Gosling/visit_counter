from flask import Flask, render_template, make_response, session
from counter import VisitCounter
from config import base
import argparse


app = Flask(__name__)
type_storage = 'sql'


@app.route('/users/')
def users_page():
    counter = VisitCounter('count_data', 'users', type_storage)
    if session == {}:
        session['id'] = counter.next_user_id()
    if session['id'] != counter.count_data['last_id']:
        counter.count_data['last_id'] = session['id']
    counter.make_count()
    counter.upload_metadata('users', session['id'])
    return render_template('index.html', **counter.count_data)


@app.route('/main_page/')
def main_page():
    counter = VisitCounter('count_data', 'main_page', type_storage)
    if session == {}:
        session['id'] = counter.next_user_id()
    if session['id'] != counter.count_data['last_id']:
        counter.count_data['last_id'] = session['id']
    counter.make_count()
    counter.upload_metadata('main_page', session['id'])
    return render_template('index.html', **counter.count_data)


@app.route('/settings/')
def init_page():
    counter = VisitCounter('count_data', 'settings', type_storage)
    if session == {}:
        session['id'] = counter.next_user_id()
    if session['id'] != counter.count_data['last_id']:
        counter.count_data['last_id'] = session['id']
    counter.make_count()
    counter.upload_metadata('settings', session['id'])
    return render_template('index.html', **counter.count_data)


def main():
    global type_storage
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', default='127.0.0.1', help='web-server host')
    parser.add_argument('--port', '-p', default=5000, help='web-server port')
    parser.add_argument('--debug', '-v', default=False, help='debug app')
    parser.add_argument('--storage', '-s', default='sql',
                        help='choose sql or file storage. Example: -s file.')
    namespace = parser.parse_args()
    type_storage = namespace.storage
    app.secret_key = base.SECRET_KEY
    app.run(host=namespace.host, port=namespace.port, debug=namespace.debug)


if __name__ == '__main__':
    main()
