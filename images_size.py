# import re
# import os
# import requests
# from concurrent.futures import ThreadPoolExecutor
# import pandas as pd
#
# models_folder_path = 'models/'  # 模型文件夹路径，需要替换为正确路径
#
# def get_size(url):
#     response = requests.head(url)
#     if response.status_code == 200 and 'Content-Length' in response.headers:
#         size_bytes = int(response.headers['Content-Length'])
#         return size_bytes
#     else:
#         print(f"无法获取 URL: {url} 的大小信息")
#         return 0
#
# def process_txt_file(file_path):
#     total_size = 0
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = file.read()
#         image_urls = re.findall(r'image_url:\s(.*?)\n', data)
#
#         with ThreadPoolExecutor(max_workers=10) as executor:  # 可以根据需求调整线程数
#             sizes = list(executor.map(get_size, image_urls))
#             total_size = sum(sizes)
#
#     return total_size
#
# def main():
#     data = []
#     columns = ["文件", "图片总大小 (MB)"]
#
#     for file_name in os.listdir(models_folder_path):
#         if file_name.endswith(".txt"):
#             file_path = os.path.join(models_folder_path, file_name)
#             size = process_txt_file(file_path)
#             print(f"文件：{file_name}\n图片总大小：{size / (1024 * 1024):.2f} MB")
#             data.append([file_name, size / (1024 * 1024)])
#
#     # Create a DataFrame using pandas
#     df = pd.DataFrame(data, columns=columns)
#
#     # Export the DataFrame to an Excel file
#     df.to_excel("image_size.xlsx", index=False)
#     print("数据已写入到 image_size.xlsx 文件中")
#
# if __name__ == "__main__":
#     main()

import re
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

models_folder_path = 'models/'  # 模型文件夹路径，需要替换为正确路径

def get_size(url):
    response = requests.head(url)
    if response.status_code == 200 and 'Content-Length' in response.headers:
        size_bytes = int(response.headers['Content-Length'])
        return size_bytes
    else:
        print(f"无法获取 URL: {url} 的大小信息")
        return 0

def process_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        image_urls = re.findall(r'image_url:\s(.*?)\n', data)

        with ThreadPoolExecutor(max_workers=10) as executor:  # 可以根据需求调整线程数
            sizes = list(executor.map(get_size, image_urls))
            total_size = sum(sizes)

    return total_size

def main():
    data = []
    columns = ["文件", "图片总大小 (MB)"]

    txt_files = [file for file in os.listdir(models_folder_path) if file.endswith(".txt")]

    with ThreadPoolExecutor(max_workers=5) as executor_files:
        sizes = list(executor_files.map(process_txt_file, [os.path.join(models_folder_path, file) for file in txt_files]))

    for file_name, size in zip(txt_files, sizes):
        print(f"文件：{file_name}\n图片总大小：{size / (1024 * 1024):.2f} MB")
        data.append([file_name, size / (1024 * 1024)])

    # Create a DataFrame using pandas
    df = pd.DataFrame(data, columns=columns)

    # Export the DataFrame to an Excel file
    df.to_excel("image_size.xlsx", index=False)
    print("数据已写入到 image_size.xlsx 文件中")

if __name__ == "__main__":
    main()
