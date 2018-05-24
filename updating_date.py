# todo: aprire professional / non ho ancora capito come ottenere le credenziali...
# todo: push database

import requests
import datetime
from urllib2 import build_opener
import pymysql


connection = pymysql.connect(host='localhost', port=3306, user='root', password='mamma93', db='mercurio',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor(pymysql.cursors.DictCursor)
sql = "SELECT id, date FROM articles_prova_ansa"
cur.execute(sql)
for row in cur:
    print (row)
    '''
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO articles_prova_ansa (date_correct_type) VALUES (STR_TO_DATE('%s', " \
                    "'%%Y-%%m-%%d %%h:%%i'))"
            cursor.execute(query, [row])
            connection.commit()
    except Exception, e:
        print("Can't insert date " + str(e))
    '''