from flask import Flask, request, make_response, session
from counter import Counter

app = Flask(__name__)


@app.route('/init/')
def init_page():
    counter = Counter('visits.txt')
    count_data = {'total': 0,
                  'daily': 0,
                  'monthly': 0,
                  'yearly': 0,
                  'last_visit': '01.01.1970'}
    counter.put_json(count_data)
    return 'This is a service page. Init complete successfully'


@app.route('/')
def page():
    counter = Counter('visits.txt')
    count_data = counter.get_count()
    with open('web_html.html','r') as s:
        line = s.read()
    return line.format(count_data['total'], count_data['daily'], count_data['monthly'], count_data['yearly'])


if __name__ == '__main__':
    app.run()
