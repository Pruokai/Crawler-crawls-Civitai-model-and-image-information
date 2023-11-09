import os
import re
import requests

folder_path = 'models'  # 文件夹路径，根据实际情况进行更改
download_folder = 'models_download'  # 下载文件夹名称

# 创建下载文件夹
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 获取文件夹中所有以 .txt 结尾的文件路径
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# 遍历所有文本文件
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

        # 使用正则表达式找到所有 downloadUrl
        download_urls = re.findall(r'downloadUrl:\s*(https?://\S+)', text)

        # 下载每个 downloadUrl
        for url in download_urls:
            # 发起 GET 请求下载内容
            response = requests.get(url)

            if response.status_code == 200:
                # 获取文件名
                file_name = url.split('/')[-1]

                # 写入下载的内容到models_download文件夹中
                with open(os.path.join(download_folder, file_name), 'wb') as output_file:
                    output_file.write(response.content)
                    print(f"下载完成: {file_name}")
            else:
                print(f"无法下载: {url}")
