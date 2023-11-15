import json
import chardet
from codecs import open


# 打开原始JSON文件和新JSON文件，使用探测到的编码
with open('business_1000.json', 'r') as infile, open('yelp_academic_dataset_business_1000.json', 'w', encoding='utf-8') as outfile:
    # 逐行读取原始JSON文件
    for line in infile:
        data = json.loads(line)

        business_id = data['business_id']
        name = data['name']
        address = data['address']
        city = data['city']
        state = data['state']
        postal_code = data['postal_code']
        latitude = data['latitude']
        longitude = data['longitude']
        stars = data['stars']
        review_count = data['review_count']
        is_open = data['is_open']
        attributes = data['attributes']
        hours = data['hours']
        # 创建新的JSON数据并写入新JSON文件
        new_data = {
            'business_id': business_id,
            'name': name,
            'address': address,
            'city':city,
            'state':state,
            'postal_code':postal_code,
            'latitude':latitude,
            'longitude':longitude,
            'stars':stars,
            'review_count':review_count,
            'is_open':is_open,
            'attributes':attributes,
            'hours':hours
        }
        outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')
print("新JSON文件已创建。")
