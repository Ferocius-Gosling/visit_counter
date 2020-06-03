import functools
from flask import Flask, render_template, request
from visit_counter.counter import VisitCounter
from visit_counter import storage, errors, const
from config import base


app = Flask(__name__)
data_storage = storage.check_type(base.STORAGE_TYPE, base.CONNECT_KWARGS, base.HOSTNAME)
counter = VisitCounter(data_storage)


@app.route('/visit', methods=['POST'])
def visit():
    meta = request.get_json()
    counter.make_visit(meta['path'], meta['id'], meta['user_agent'], meta['domain'])
    return '', 204


@app.route('/stats')
def stats():
    yearly = counter.get_stats(const.TimeSection.yearly)
    monthly = counter.get_stats(const.TimeSection.monthly)
    weekly = counter.get_stats(const.TimeSection.weekly)
    daily = counter.get_stats(const.TimeSection.daily)
    hourly = counter.get_stats(const.TimeSection.hourly)
    total = counter.get_stats(const.TimeSection.total)
    unique = counter.get_unique_user_stats()
    return render_template('index.html',
                           yearly=yearly,
                           monthly=monthly,
                           weekly=weekly,
                           daily=daily,
                           hourly=hourly,
                           total=total,
                           last_id=unique)
