import json
import pymysql
import time
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s" % data[0])  # 结果表明已经连接成功
    cursor.execute("DROP TABLE IF EXISTS checkin")
    sql = """CREATE TABLE checkin (
    business_id VARCHAR(22) NOT NULL,
    date LONGTEXT,
    PRIMARY KEY (business_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
    )"""
    cursor.execute(sql)

def reviewdata_insert(db):
    with open('checkin_1000.json', encoding='utf-8') as f:
        i = 0
        while True:
            i += 1
            lines = f.readline()
            if not lines:
                break  # 如果没有更多的行可读，结束循环
            if not lines.strip():  # 检查是否为空行
                continue
            try:
                data = json.loads(lines)
                result = [(data['business_id'], data['date'])]
                insert_sql = "INSERT INTO checkin (business_id, date) VALUES (%s, %s)"
                cursor = db.cursor()
                try:
                    cursor.executemany(insert_sql, result)
                    print(u'正在载入第%s行......' % i)
                    print(result)
                    db.commit()
                except pymysql.IntegrityError as e:
                    if "foreign key constraint fails" not in str(e):
                        print(f"Error inserting data: {str(e)}")
                        db.rollback()
                except Exception as e:
                    print(f"Error processing line {i}: {str(e)}")
                    db.rollback()

            except Exception as e:
                db.rollback()
                print(str(e))
                break

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '631625308',
    'database': 'yelp_origin'
}

db = pymysql.connect(**db_config)
cursor = db.cursor()
prem(db)
start = time.time()
reviewdata_insert(db)
end = time.time()
time = end - start
print(f'耗时：{time}s')
cursor.close()
