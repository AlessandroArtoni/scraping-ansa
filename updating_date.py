
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
    date = row['date']
    print (date)
    idRow = int(row['id'])
    print(idRow)
    if row['id'] < 38914:
        try:
            with connection.cursor() as cursor:
                query = "UPDATE `articles_prova_ansa` SET `date_correct_type` = " \
                        "(STR_TO_DATE('`%s`','`%%Y-%%m-%%d %%H:%%i`')) WHERE `articles_prova_ansa.id` = `%s`"
                cursor.execute(query, [date, idRow])
                connection.commit()
        except Exception, e:
            print("Can't insert date " + str(e))
