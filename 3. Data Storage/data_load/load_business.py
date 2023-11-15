import json
import pymysql
import time
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s" % data[0])  # 结果表明已经连接成功
    cursor.execute("DROP TABLE IF EXISTS business")
    sql = """CREATE TABLE business (
    business_id VARCHAR(22) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(255),
    state CHAR(2),
    postal_code VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT,
    stars FLOAT,
    review_count INT,
    is_open TINYINT(1),
    attributes text,
    hours text,
    PRIMARY KEY (business_id)
    )"""
    cursor.execute(sql)

def reviewdata_insert(db):
    with open('business_1000.json', encoding='utf-8') as f:
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
                print(u'正在载入第%s行......' % i)
                result = [(data['business_id'], data['name'], data['address'], data['city'], data['state'], data['postal_code'], data['latitude'], data['longitude'], data['stars'], data['review_count'], data['is_open'], json.dumps(data.get('attributes')),json.dumps(data.get('hours')))]
                print(result)

                insert_sql = "INSERT INTO business (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor = db.cursor()
                cursor.executemany(insert_sql, result)
                db.commit()
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
