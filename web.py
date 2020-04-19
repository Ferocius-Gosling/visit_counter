from flask import Flask, render_template, make_response, request, session
from counter import VisitCounter
import argparse


app = Flask(__name__)
type_storage = 'sql'


counter = VisitCounter(storage_type='enum.Value', storage_params={})

# клиентская часть
# javascript-код который отправляет запрос на сервер при посещении странице
# он должен проставлять cookie user_id пользователю если ее нет
# защитится от накрутки, установив cookie с временем жизни
# серверная часть
@app.route('/visit', methods=['GET'])
def visit():
    """
    Записывает очерередное посещение с указанными мета-данными
    URI параметры: (example: http://visit-counter.ru/visit?user_id=id&...)

     - user_id - идентификатор пользователя (uuid)
     - domain - сам сайт, который считает посещения
     - path - путь до страницы на сайте, которую посетли
     - user_agent - информация о браузере
    """
    counter.increment(*params)
    return '', 204


@app.route('/stats', )
def stats():
    """
    Возвращает статистику посещений.
    Возможные фильтры (URI параметры)
     - по дате
     - пользователю
     - по браузеру
     - домену
     - странице
    """
    return counter.get_stats(fitlters=...), 200

@app.route('/users/')
def users_page():

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
    app.run(host=namespace.host, port=namespace.port, debug=namespace.debug)


if __name__ == '__main__':
    main()
