import time
import requests
import os
from concurrent.futures import ThreadPoolExecutor

params = {
    'limit': 100,
    # 可以根据需要添加其他查询参数
}

url = 'https://civitai.com/api/v1/images'

all_images_data = []  # 存储所有图像数据的列表

total_pages = 2  # 想要爬取的页数

for page in range(1, total_pages + 1):
    params['page'] = page  # 更新参数中的页面数

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        images = data.get('items', [])

        if images:
            all_images_data.extend(images)
        else:
            break  # 如果没有更多图像数据时跳出循环
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        break

# 创建一个文件夹用于存放单独的图像数据文件
folder_name = 'images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def write_image_data(image_data):
    image_id = image_data.get('id')
    file_path = os.path.join(folder_name, f'{image_id}.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
        image_id = image_data.get('id')
        image_url = image_data.get('url')
        image_hash = image_data.get('hash')
        image_width = image_data.get('width')
        image_height = image_data.get('height')
        is_nsfw = image_data.get('nsfw')
        nsfw_level = image_data.get('nsfwLevel')
        created_at = image_data.get('createdAt')
        post_id = image_data.get('postId')
        stats = image_data.get('stats', {})
        cryCount = stats.get('cryCount')
        laughCount = stats.get('laughCount')
        likeCount = stats.get('likeCount')
        dislikeCount = stats.get('dislikeCount')
        heartCount = stats.get('heartCount')
        commentCount = stats.get('commentCount')
        meta = image_data.get('meta', {})
        if meta is not None:
            Size = meta.get('Size')
            seed = meta.get('seed')
            Model = meta.get('Model')
            steps = meta.get('steps')
            prompt = meta.get('prompt')
            sampler = meta.get('sampler')
            cfgScale = meta.get('cfgScale')
            Clipskip = meta.get('Clip skip')
            Hiresupscale = meta.get('Hires upscale')
            Hiresupscaler = meta.get('Hires upscaler')
            negativePrompt = meta.get('negativePrompt')
            Denoisingstrength = meta.get('Denoising strength')
        username = image_data.get('username')

        # 写入数据到文件
        file.write(f"Image ID: {image_id}\n")
        file.write(f"Image URL: {image_url}\n")
        file.write(f"Image Hash: {image_hash}\n")
        file.write(f"Image Width: {image_width}\n")
        file.write(f"Image Height: {image_height}\n")
        file.write(f"NSFW: {is_nsfw}\n")
        file.write(f"NSFW Level: {nsfw_level}\n")
        file.write(f"Created At: {created_at}\n")
        file.write(f"Post ID: {post_id}\n")
        file.write(f"Cry Count: {cryCount}\n")
        file.write(f"Laugh Count: {laughCount}\n")
        file.write(f"Like Count: {likeCount}\n")
        file.write(f"Dislike Count: {dislikeCount}\n")
        file.write(f"Heart Count: {heartCount}\n")
        file.write(f"Comment Count: {commentCount}\n")
        file.write(f"Size: {Size}\n")
        file.write(f"Seed: {seed}\n")
        file.write(f"Model: {Model}\n")
        file.write(f"Steps: {steps}\n")
        file.write(f"Prompt: {prompt}\n")
        file.write(f"Sampler: {sampler}\n")
        file.write(f"CfgScale: {cfgScale}\n")
        file.write(f"Clip Skip: {Clipskip}\n")
        file.write(f"Hires Upscale: {Hiresupscale}\n")
        file.write(f"Hires Upscaler: {Hiresupscaler}\n")
        file.write(f"Negative Prompt: {negativePrompt}\n")
        file.write(f"Denoising Strength: {Denoisingstrength}\n")
        file.write(f"Username: {username}\n\n")
        time.sleep(5)

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(write_image_data, all_images_data)
