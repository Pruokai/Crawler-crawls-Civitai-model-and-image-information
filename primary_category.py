import pandas as pd
import os
import re
import string

def clean_text(text):
    # 使用正则表达式删除 HTML 标签
    clean_text = re.sub(r'<.*?>', '', text)
    # 删除不可打印字符
    clean_text = ''.join(filter(lambda x: x in string.printable, clean_text))
    return clean_text

folder_path = 'models'  # 更新为您的文件夹路径
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

data_list = []
model_keys = [
    'Model ID', 'Model Name', 'Model Description', 'Model Type', 'NSFW', 'Allow No Credit',
    'Allow Commercial Use', 'Allow Derivatives', 'Creator Username', 'Download Count', 'Favorite Count',
    'Comment Count', 'Rating Count', 'Rating', 'updatedAt', 'baseModel'
]

current_model_data = {}

# 遍历每个文件并提取一级类目数据
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if key in model_keys:
                    # Clean the 'value' before storing
                    value = clean_text(value)
                    current_model_data[key] = value

                    # Extract baseModel and updatedAt
                    if key == 'updatedAt':
                        current_model_data['updatedAt'] = re.search(r': (.+)', line).group(1)
                    if key == 'baseModel':
                        current_model_data['baseModel'] = re.search(r': (.+)', line).group(1)

        if current_model_data:  # 如果当前模型数据不为空
            data_list.append(current_model_data)
            current_model_data = {}

# 创建一级类目表
primary_table = pd.DataFrame(data_list)

output_file_primary = 'praimary_category.xlsx'
primary_table.to_excel(output_file_primary, index=False)
