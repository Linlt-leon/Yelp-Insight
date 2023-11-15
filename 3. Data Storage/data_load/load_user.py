import json
import pymysql
import time
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s" % data[0])  # 结果表明已经连接成功
    cursor.execute("DROP TABLE IF EXISTS user")
    sql = """CREATE TABLE user (
    user_id VARCHAR(22) NOT NULL,
    name VARCHAR(255) NOT NULL,
    review_count int,
    yelping_since text,
    useful int,
    funny int,
    cool int,
    elite text,
    fans int,
    average_stars float,
    compliment_hot int,
    compliment_more int,
    compliment_profile int,
    compliment_cute int,
    compliment_list int,
    compliment_note int,
    compliment_plain int,
    compliment_cool int,
    compliment_funny int,
    compliment_writer int,
    compliment_photos int,
    PRIMARY KEY (user_id)
    )"""
    cursor.execute(sql)

def reviewdata_insert(db):
    with open('user_1000.json', encoding='utf-8') as f:
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
                result = [(data['user_id'], data['name'], data['review_count'], data['yelping_since'], data['useful'], data['funny'], data['cool'], data['elite'], data['fans'], data['average_stars'], data['compliment_hot'] ,data['compliment_more'] ,data['compliment_profile'] ,data['compliment_cute'] ,data['compliment_list'] ,data['compliment_note'] ,data['compliment_plain'] ,data['compliment_cool'] ,data['compliment_funny'] ,data['compliment_writer'] ,data['compliment_photos'])]
                print(result)

                insert_sql = "INSERT INTO user (user_id, name, review_count, yelping_since, useful, funny, cool, elite, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
