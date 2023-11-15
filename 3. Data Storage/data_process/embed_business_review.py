import json
import time
t1=time.time()
# 读取business和review JSON文件
with open('business_1000.json', 'r', encoding='utf-8') as business_file:
    business_data = [json.loads(line) for line in business_file]

with open('yelp_academic_dataset_review.json', 'r', encoding='utf-8') as review_file:
    review_data = [json.loads(line) for line in review_file]

# 创建一个新的business_new JSON数据
business_new_data = []

# 遍历business数据
for business_entry in business_data:
    # 获取当前business行的business_id
    current_business_id = business_entry['business_id']

    # 在review数据中查找与当前business_id相同的所有行
    related_reviews = [review_entry for review_entry in review_data if review_entry['business_id'] == current_business_id]

    # 在当前business行数据中增加一个名为'review'的键，其值为相关的review数据
    business_entry['review'] = related_reviews

    # 将当前business行数据添加到新的business_new数据中
    business_new_data.append(business_entry)

# 将生成的business_new数据写入新的JSON文件
with open('business_new.json', 'w', encoding='utf-8') as business_new_file:
    json.dump(business_new_data, business_new_file, indent=2, ensure_ascii=False)
t2=time.time()
print(f'time is {t2-t1} s')