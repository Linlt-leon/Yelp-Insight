import json

# 打开原始JSON文件和新的JSON文件
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/archive/yelp_academic_dataset_tip.json', 'r', encoding='utf-8') as input_file, open(
        'tip_5000.json', 'w', encoding='utf-8') as output_file:
    new_data = []

    # 逐行读取原始JSON文件
    for line in input_file:
        try:
            json_obj = json.loads(line)
            new_data.append(json_obj)
        except json.JSONDecodeError:
            # 如果行不是合法的JSON对象，跳过
            pass

        # 如果已经读取了前10个JSON对象，停止读取
        if len(new_data) >= 5000:
            break

    # 写入新的JSON文件，每行一个JSON对象，除了最后一个对象
    for i, json_obj in enumerate(new_data):
        output_file.write(json.dumps(json_obj, ensure_ascii=False))
        if i < len(new_data) - 1:
            output_file.write('\n')
