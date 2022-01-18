import pymysql;


db = pymysql.connect(host='localhost',
                        user='caizijian',
                        password='Czj1212112',
                        database = 'Flask')


cursor = db.cursor()

try:
    cursor.execute("INSERT INTO UserAccount VALUES ('caizijian2','1234tttt', false);")
    results = cursor.fetchone()
    print(results)
except:
    print("wrong data")

db.close()