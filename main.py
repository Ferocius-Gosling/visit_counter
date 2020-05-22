import argparse
from config import base
from visit_counter import const


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', default='127.0.0.1', help='web-server host')
    parser.add_argument('--port', '-p', default=5000, help='web-server port')
    parser.add_argument('--debug', '-v', default=False, help='debug app')
    parser.add_argument('--storage', '-s', default='sql',
                        help='choose sql or file storage. Example: -s file.')
    namespace = parser.parse_args()
    base.STORAGE_TYPE = const.StorageType(namespace.storage)
    base.HOSTNAME = namespace.host

    from visit_counter.web import app

    app.secret_key = base.SECRET_KEY
    app.run(host=namespace.host, port=namespace.port, debug=namespace.debug)


if __name__ == '__main__':
    main()