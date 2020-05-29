from flask import Flask, render_template, request
from visit_counter.counter import VisitCounter
from config import base


app = Flask(__name__)
counter = VisitCounter(base.HOSTNAME, base.STORAGE_TYPE, base.CONNECT_KWARGS)


@app.route('/visit', methods=['POST'])
def visit():
    meta = request.get_json()
    counter.make_visit(meta['path'], meta['id'], meta['user_agent'], meta['domain'], meta['is_new'])
    return '', 204


@app.route('/stats')
def stats():
    stat = counter.get_stats('path', '/stats')
    return render_template('index.html', **stat)
