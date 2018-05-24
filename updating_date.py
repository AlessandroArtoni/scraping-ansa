
import requests
import datetime
from urllib2 import build_opener
import pymysql

connection = pymysql.connect(host='localhost', port=3306, user='root', password='mamma93', db='mercurio',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor(pymysql.cursors.DictCursor)
# change this to select the right table
sql = "SELECT id, date FROM articles_ansa"
cur.execute(sql)
for row in cur:
    # the following lines are used to format properly the date we want to create
    print (row)
    date = row['date']
    idRow = int(row['id'])
    day = date[0:2]
    month = date[3:5]
    year = date[6:10]
    time = date[11:16]
    date = year+'-'+month+'-'+day+' '+time
    try:
        with connection.cursor() as cursor:
            # check consistency in up, set and where
            query = "UPDATE articles_ansa SET data_mod = " \
                    "STR_TO_DATE(%s,'%%Y-%%m-%%d %%H:%%i') WHERE articles_ansa.id = %s"
            cursor.execute(query, [date, idRow])
            connection.commit()
    except Exception, e:
        print("Can't insert date " + str(e))

print ("End of the program.")
