import json
import pymysql
import time
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s" % data[0])  # 结果表明已经连接成功
    cursor.execute("DROP TABLE IF EXISTS tip")
    sql = """CREATE TABLE tip (
    user_id VARCHAR(22) NOT NULL,
    business_id VARCHAR(22) NOT NULL,
    text VARCHAR(600),
    date VARCHAR(100),
    compliment_count int,
    PRIMARY KEY (user_id,business_id,text,date,compliment_count),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
    )"""
    cursor.execute(sql)

def tipdata_insert(db):
    with open('yelp_academic_dataset_tip.json', encoding='utf-8') as f:
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

                result = [(data['user_id'], data['business_id'], data['text'], data['date'], data['compliment_count'])]


                insert_sql = "INSERT INTO tip (user_id, business_id, text, date, compliment_count) VALUES (%s, %s, %s, %s, %s)"
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
tipdata_insert(db)
end = time.time()
time = end - start
print(f'耗时：{time}s')
cursor.close()
