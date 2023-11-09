import os
import requests
from concurrent.futures import ThreadPoolExecutor
import hashlib
import re

models_folder_path = 'models/'  # 模型文件夹路径，需要替换为正确路径
images_download_folder = 'images_download'  # 图片下载文件夹名称

def download_image(image_url):
    response = requests.get(image_url)

    if response.status_code == 200:
        image_data = response.content
        md5_hash = hashlib.md5(image_data).hexdigest()
        file_path = f"{images_download_folder}/{md5_hash[0]}/{md5_hash[1]}/{md5_hash[2]}/{md5_hash[3]}/{md5_hash}.jpeg"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 创建多级目录

        with open(file_path, "wb") as file:
            file.write(image_data)
            print(f"图片已成功下载并存储：{file_path}")
    else:
        print("无法下载图片。")

def process_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        image_urls = re.findall(r'image_url:\s(.*?)\n', data)

        with ThreadPoolExecutor(max_workers=10) as executor:  # 可以根据需求调整线程数
            executor.map(download_image, image_urls)

def main():
    for file_name in os.listdir(models_folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(models_folder_path, file_name)
            process_txt_file(file_path)
            print(f"文件：{file_name}\n图片下载完成")

if __name__ == "__main__":
    # 创建图片下载文件夹
    os.makedirs(images_download_folder, exist_ok=True)

    main()
