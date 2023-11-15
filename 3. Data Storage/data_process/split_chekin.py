import json

# 打开原始JSON文件和新JSON文件
with open('yelp_academic_dataset_checkin.json', 'r') as infile, open('yelp_academic_dataset_checkin_new.json', 'w') as outfile:
    # 逐行读取原始JSON文件
    for line in infile:
        data = json.loads(line)
        business_id = data['business_id']
        dates = data['date'].split(', ')  # 拆分日期字符串

        # 创建新的JSON数据并写入新JSON文件
        for date in dates:
            new_data = {
                'business_id': business_id,
                'date': date
            }
            outfile.write(json.dumps(new_data) + '\n')

print("新JSON文件已创建。")
