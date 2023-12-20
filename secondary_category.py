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
model_version_keys = [
    'name', 'id', 'createdAt', 'updatedAt', 'trainedWords', 'baseModel', 'description',
    'downloadCount', 'ratingCount', 'rating', 'sizeKB', 'type', 'downloadUrl',  'primary', 'SHA256'
]

current_model_data = {}
current_version_data = {}
is_files_section = False  # 新增一个标志，表示当前处理的是 files 部分

# 遍历每个文件并提取二级类目数据
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if key in model_version_keys:
                    value = clean_text(value)
                    current_version_data[key] = value

                if key == 'id':
                    if is_files_section:
                        current_model_data['id'] = value
                    else:
                        current_version_data['Version_ID'] = value  # 将第一个 "id" 改为 "Version_ID"

                if key == 'Model ID':
                    current_model_data = {key: value}

                if key == 'files':
                    is_files_section = True

                # 在这里添加对 files 中 name 的处理
                if key == 'name':
                    if is_files_section:
                        current_model_data['name'] = value.strip()
                    else:
                        current_version_data['version'] = value.strip()

                if key == 'primary' and current_version_data:
                    if current_version_data.get('name', '').strip() != '':
                        data = {**current_model_data, **current_version_data}
                        data_list.append(data)
                    current_version_data = {}
                    is_files_section = False  # 处理完 files 部分后重置标志

        if current_version_data:
            if current_version_data.get('name', '').strip() != '':
                data = {**current_model_data, **current_version_data}
                data_list.append(data)
            current_version_data = {}
            is_files_section = False  # 处理完 files 部分后重置标志

# 创建二级类目表
secondary_table = pd.DataFrame(data_list)

output_file_secondary = 'secondary_category.xlsx'
secondary_table.to_excel(output_file_secondary, index=False)
