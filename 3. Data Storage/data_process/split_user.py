import json
import chardet
from codecs import open

# 用 chardet 探测文件编码
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# 获取文件编码
file_encoding = detect_file_encoding('yelp_academic_dataset_user.json')

# 打开原始JSON文件和新JSON文件，使用探测到的编码
with open('yelp_academic_dataset_user.json', 'r', encoding=file_encoding) as infile, open('yelp_academic_dataset_friend.json', 'w', encoding='utf-8') as outfile:
    # 逐行读取原始JSON文件
    for line in infile:
        data = json.loads(line)
        user_id = data['user_id']
        friends = data['friends'].split(', ')  # 拆分日期字符串

        # 创建新的JSON数据并写入新JSON文件
        for friend in friends:
            new_data = {
                'user_id': user_id,
                'friend': friend
            }
            outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')

print("新JSON文件已创建。")
