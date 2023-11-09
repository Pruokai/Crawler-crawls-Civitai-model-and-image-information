import pandas as pd
import os
import re
from unidecode import unidecode


def remove_non_ascii(text):
    # 过滤非ASCII字符和特殊符号
    return ''.join(i for i in text if 31 < ord(i) < 127)


def remove_non_printable_chars(cell):
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', str(cell))


# 图像数据的关键字段
image_keys = [
    'id', 'image_url', 'nsfw', 'width', 'height', 'hash', 'Size', 'seed', 'Model', 'steps',
    'prompt', 'sampler', 'cfgScale', 'resources', 'Clip skip', 'Hires upscale', 'Hires upscaler',
    'negativePrompt', 'Denoising strength'
]

# 循环遍历 9 个文件夹
for folder_number in range(1, 10):
    folder_path = f'models{folder_number}'  # 文件夹路径 models1 至 models9

    # 准备每个文件夹的输出文件名
    output_file = f'tertiary_category{folder_number}.xlsx'

    # 获取文件夹中所有以 .txt 结尾的文件路径
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

    data_frames = []

    for file_path in file_paths:
        data_list = []

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            current_image_data = {}
            current_model_data = {}
            current_name = None

            for line in lines:
                line = line.strip()
                if line != '':
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()

                        if key == 'Model':
                            current_model_data = {key: value}

                        if key == 'name':
                            if value != '':
                                current_name = remove_non_ascii(value)  # 移除非ASCII字符

                        if key in image_keys:
                            if key == 'name' and current_name is not None:
                                value = current_name
                            value = remove_non_ascii(value)  # 移除非ASCII字符
                            current_image_data[key] = value

                        if key == 'Denoising strength':
                            if current_image_data:
                                data = {**{'name': current_name}, **current_model_data, **current_image_data}
                                data_list.append(data)
                                current_image_data = {}
                                current_model_data = {}

        df = pd.DataFrame(data_list)
        df = df.apply(lambda col: col.apply(remove_non_printable_chars))
        data_frames.append(df)

    # 合并数据框并将数据写入到每个文件夹对应的 Excel 文件中
    combined_df = pd.concat(data_frames)

    with pd.ExcelWriter(output_file) as writer:
        combined_df.to_excel(writer, index=False, sheet_name='Combined_Data')
