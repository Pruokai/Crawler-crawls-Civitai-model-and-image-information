# 存入表格
import re
import os
import pandas as pd


# 文件夹路径
path = "models"

# 列出目录中的所有文件
files = os.listdir(path)

# 用于匹配所需信息的正则表达式模式
pattern = r"files:\s+name:\s+([^\n]+)\n\s+id:\s+([^\n]+)\n\s+sizeKB:\s+([^\n]+)"

# 初始化存储数据的列表
data = []

# 遍历目录中的每个文件
for file_name in files:
    file_path = os.path.join(path, file_name)
    if file_name.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            matches = re.findall(pattern, text)
            for match in matches:
                if all(item is not None for item in match):
                    name, file_id, size_kb = match
                    if size_kb is not None and size_kb != 'None':
                        size_kb = float(size_kb)
                        size_mb = size_kb / 1024
                        data.append([file_name, name, file_id, size_mb])
                    else:
                        # 在没有有效文件大小的情况下继续循环下一个匹配
                        continue


# 创建 Pandas DataFrame
df = pd.DataFrame(data, columns=['文件', '模型名字', '模型ID', '模型大小(MB)'])

# 转换 '模型ID' 列为数字类型
df['模型ID'] = pd.to_numeric(df['模型ID'], errors='coerce')

# 将数据存储为 Excel 文件
excel_file = 'model_size.xlsx'
df.to_excel(excel_file, index=False)
print(f"数据已存储到 {excel_file} 文件")