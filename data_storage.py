import pymysql


class AbstractStorage:
    def __init__(self, file_data, way_from):
        self.file_data = pymysql.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         db=file_data,
                                         cursorclass=pymysql.cursors.DictCursor)
        self._keys_count_data = ['total', 'yearly', 'monthly',
                                 'daily', 'last_id', 'way_from', 'last_visit']
        self.way_from = way_from

    def load_data(self, file_from):
        with self.file_data:
            cur = self.file_data.cursor()
            cur.execute('SELECT * FROM ' + file_from + ' WHERE way_from=' + '\'' + self.way_from + '\'')
            count_data = cur.fetchall()[0]
        return count_data

    def update_data(self, count_data):
        with self.file_data:
            cur = self.file_data.cursor()
            query = 'UPDATE count_visits SET '
            where = ' WHERE way_from=\'' + self.way_from + "'"
            for key in self._keys_count_data:
                if key == 'way_from' or key == 'last_visit':
                    cur.execute(query + key+'=' + "'{}'".format(count_data[key]) + where)
                else:
                    cur.execute(query + key+'='+'{}'.format(count_data[key]) + where)

    def insert_data(self, user_id, date, way):
        with self.file_data:
            cur = self.file_data.cursor()
            query = "INSERT INTO user_visits (way_from, user_id, date_visit) VALUE "
            value = "('{}',{},'{}')".format(way, user_id, date)
            cur.execute(query + value)
