import pandas as pd
import os

folder_path = 'models'  # 更新为您的文件夹路径
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

data_list = []
model_version_keys = [
    'id', 'name', 'createdAt', 'updatedAt', 'trainedWords', 'baseModel', 'description',
    'downloadCount', 'ratingCount', 'rating', 'sizeKB', 'type', 'downloadUrl', 'primary'
]

current_model_data = {}
current_version_data = {}

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
                    current_version_data[key] = value

                if key == 'Model ID':  # 用 Model ID 作为连接的桥梁
                    current_model_data = {key: value}

                if key == 'primary' and current_version_data:
                    if current_version_data.get('name', '').strip() != '':
                        data = {**current_model_data, **current_version_data}
                        data_list.append(data)
                    current_version_data = {}

        if current_version_data:
            if current_version_data.get('name', '').strip() != '':
                data = {**current_model_data, **current_version_data}
                data_list.append(data)
            current_version_data = {}

# 创建二级类目表
secondary_table = pd.DataFrame(data_list)

output_file_secondary = 'secondary_category.xlsx'
secondary_table.to_excel(output_file_secondary, index=False)

