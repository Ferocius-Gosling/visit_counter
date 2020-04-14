import pymysql
import json


class AbstractStorage:
    def __init__(self, file_data):
        self.file_data = pymysql.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         db=file_data,
                                         charpipset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

    def load_data(self, file_from, way_from):
        with self.file_data:
            cur = self.file_data.cursor()
            cur.execute('SELECT * FROM ' + file_from + ' WHERE way_from=' + way_from)
            count_data = cur.fetchall()
        return count_data
       # try:
        #    with open(self.file_data, 'r') as load_file:
         #       return json.load(load_file)
       # except:
        #    with open(self.file_data, 'w') as load_file:
         #       count_data = {'total': 0,
          #                            'daily': 0,
           #                           'monthly': 0,
            #                          'yearly': 0,
             #                         'ids': [],
              #                        'last_id': 0,
               #                       'last_visit': '01.01.1970'}
               # json.dump(count_data, load_file)
               # return count_data

    def update_data(self, count_data, key_last_id=False):
        with self.file_data:
            cur = self.file_data.cursor()
            for key in count_data.keys:
                if key == 'last_id':
                    continue
                cur.execute('UPDATE count_visits SET '+key+'='+'{}'.format(count_data[key]))

    def insert_data(self, id, date, way):
        with self.file_data:
            cur = self.file_data.cursor()
            query = 'INSERT INTO user_visits (way_from, user_id, date_visit) VALUE ('
            value = way + ",\"" + id + ",\"" + date + "\")"
            cur.execute(query + value)
