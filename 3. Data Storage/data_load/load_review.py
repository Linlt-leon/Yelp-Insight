import json
import pymysql
import time

def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s" % data[0])
    cursor.execute("DROP TABLE IF EXISTS review")
    sql = """CREATE TABLE review (
    review_id VARCHAR(22) NOT NULL,
    user_id VARCHAR(22) NOT NULL,
    business_id VARCHAR(22) NOT NULL,
    stars INT,
    date TEXT,
    text TEXT,
    useful int,
    funny int,
    cool int,
    PRIMARY KEY (review_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
    )"""
    cursor.execute(sql)

def reviewdata_insert(db):
    with open('review_1000.json', encoding='utf-8') as f:
        i = 0
        while True:
            i += 1
            lines = f.readline()
            if not lines:
                break
            if not lines.strip():
                continue
            try:
                data = json.loads(lines)

                result = [(data['review_id'], data['user_id'], data['business_id'], data['stars'], data['date'], data['text'], data['useful'], data['funny'], data['cool'])]

                insert_sql = "INSERT INTO review (review_id, user_id, business_id, stars, date, text, useful, funny, cool) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
                print(f"Error processing line {i}: {str(e)}")
                db.rollback()


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
elapsed_time = end - start
print(f'耗时：{elapsed_time}s')
cursor.close()
