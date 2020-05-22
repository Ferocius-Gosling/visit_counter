from flask import Flask, render_template, request, make_response
from visit_counter.counter import VisitCounter
from config import base
import uuid


app = Flask(__name__)
type_storage = base.STORAGE_TYPE
counter = VisitCounter('count_data', base.HOSTNAME, type_storage)


@app.route('/visit', methods=['POST'])
def visit():
    # user_id = request.cookies.get('user_id')
    # random_uuid = uuid.uuid4()
    # if user_id is None:
    #     new_user_id = str(uuid.uuid4())
    #     if user_id != new_user_id:
    #         counter.unique_user_increment()
    #     make_response().set_cookie('user_id', new_user_id, max_age=60*60*24)
    #     user_id = new_user_id
    meta = request.get_json()
    counter.make_visit(meta['path'], meta['id'], meta['user_agent'], meta['domain'], meta['is_new'])
    return '', 204


@app.route('/stats')
def stats():
    stat = counter.get_stats('path','/stats')
    return render_template('index.html', **stat)


# @app.route('/users/')
# def users_page():
#     counter = VisitCounter('count_data', 'users', type_storage)
#     if session == {}:
#         session['id'] = counter.next_user_id()
#     if session['id'] != counter.count_data['last_id']:
#         counter.count_data['last_id'] = session['id']
#     counter.make_count()
#     counter.upload_metadata('users', session['id'])
#     return render_template('index.html', **counter.count_data)
#
#
# @app.route('/main_page/')
# def main_page():
#     counter = VisitCounter('count_data', 'main_page', type_storage)
#     if session == {}:
#         session['id'] = counter.next_user_id()
#     if session['id'] != counter.count_data['last_id']:
#         counter.count_data['last_id'] = session['id']
#     counter.make_count()
#     counter.upload_metadata('main_page', session['id'])
#     return render_template('index.html', **counter.count_data)
#
#
# @app.route('/settings/')
# def init_page():
#     counter = VisitCounter('count_data', 'settings', type_storage)
#     if session == {}:
#         session['id'] = counter.next_user_id()
#     if session['id'] != counter.count_data['last_id']:
#         counter.count_data['last_id'] = session['id']
#     counter.make_count()
#     counter.upload_metadata('settings', session['id'])
#     return render_template('index.html', **counter.count_data)
