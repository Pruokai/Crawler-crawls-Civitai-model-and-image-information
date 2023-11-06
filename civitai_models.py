import requests
import time
import os
import threading
import queue

url = 'https://civitai.com/api/v1/models'
params = {
    'limit': 100, # 你可以根据需要更改 limit 数量
    'sort': 'Newest'
}
total_pages = 830  # 想要爬取的页数

lock = threading.Lock()  # 创建一个锁以同步文件写入

def fetch_data(page):
    params['page'] = page  # 更新参数中的页面数
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        models = data.get('items', [])

        if models:
            process_models(models)
        else:
            return

def process_models(models):
    # 分类和处理模型数据
    for model in models:
        model_id = model.get('id')
        model_name = model.get('name')
        model_description = model.get('description')
        model_type = model.get('type')
        nsfw = model.get('nsfw')
        allow_no_credit = model.get('allowNoCredit')
        allow_commercial_use = model.get('allowCommercialUse')
        allow_derivatives = model.get('allowDerivatives')
        creator_username = model.get('creator', {}).get('username')
        download_count = model.get('stats', {}).get('downloadCount')
        favorite_count = model.get('stats', {}).get('favoriteCount')
        comment_count = model.get('stats', {}).get('commentCount')
        rating_count = model.get('stats', {}).get('ratingCount')
        rating = model.get('stats', {}).get('rating')
        tags = model.get('tags', [])
        modelVersiones = model.get('modelVersions',[])
        all_modelVersiones_info = []
        for modelVersions in modelVersiones:
            modelVersions_id = modelVersions.get('id')
            modelVersions_modelId = modelVersions.get('modelId')
            modelVersions_name = modelVersions.get('name')
            modelVersions_createdAt = modelVersions.get('createrAt')
            modelVersions_updatedAt = modelVersions.get('updatedAt')
            modelVersions_trainedWords = modelVersions.get('trainedWords',[])
            modelVersions_baseModel = modelVersions.get('baseModel')
            modelVersions_earlyAccessTimeFrame = modelVersions.get('earlyAccessTimeFrame')
            modelVersions_description = modelVersions.get('description')
            modelVersions_stats = modelVersions.get('stats',{})
            stats_downloadCount = modelVersions_stats.get('downloadCount')
            stats_ratingCount = modelVersions_stats.get('ratingCount')
            stats_rating = modelVersions_stats.get('rating')
            modelVersions_filesd = modelVersions.get('files',[])
            for modelVersions_files in modelVersions_filesd:
                files_name = modelVersions_files.get('name')
                files_id = modelVersions_files.get('id')
                files_sizeKB = modelVersions_files.get('sizeKB')
                files_type = modelVersions_files.get('type')
                files_metadata = modelVersions_files.get('metadata',{})
                if files_metadata is not None:
                    metadata_fp = files_metadata.get('fp')
                    metadata_size = files_metadata.get('size')
                    metadata_format = files_metadata.get('format')
                files_pickleScanResult = modelVersions_files.get('pickleScanResult')
                files_pickleScanMessage = modelVersions_files.get('pickleScanMessage')
                files_virusScanResult = modelVersions_files.get('virusScanResult')
                files_scannedAt = modelVersions_files.get('scannedAt')
                files_hashes = modelVersions_files.get('hashes',{})
                if files_hashes is not None:
                    hashes_AutoV2 = files_hashes.get('AutoV2')
                    hashes_SHA256 = files_hashes.get('SHA256')
                    hashes_CRC32 = files_hashes.get('CRC32')
                    hashes_BLAKE3 = files_hashes.get('BLAKE3')
                files_downloadUrl = modelVersions_files.get('downloadUrl')
                files_primary = modelVersions_files.get('primary')
            image_datas = modelVersions.get('images')
            all_images_info = []  # 创建一个空列表，用于存储所有图片信息
            for image_data in image_datas:
                id = image_data.get('id')
                image_url = image_data.get('url')
                nsfw = image_data.get('nsfw')
                width = image_data.get('width')
                height = image_data.get('height')
                hash = image_data.get('hash')
                meta = image_data.get('meta', {})
                Size = None
                seed = None
                Model = None
                steps = None
                prompt = None
                sampler = None
                cfgScale = None
                resources = None
                Clipskip = None
                Hiresupscale = None
                Hiresupscaler = None
                negativePrompt = None
                Denoisingstrength = None
                if meta is not None:
                    Size = meta.get('Size')
                    seed = meta.get('seed')
                    Model = meta.get('Model')
                    steps = meta.get('steps')
                    prompt = meta.get('prompt')
                    sampler = meta.get('sampler')
                    cfgScale = meta.get('cfgScale')
                    resources = meta.get('resources', [])
                    Clipskip = meta.get('Clip skip')
                    Hiresupscale = meta.get('Hires upscale')
                    Hiresupscaler = meta.get('Hires upscaler')
                    negativePrompt = meta.get('negativePrompt')
                    Denoisingstrength = meta.get('Denoising strength')
                # 创建包含所有信息的字典
                image_info = {
                    'id': id,
                    'image_url': image_url,
                    'nsfw': nsfw,
                    'width': width,
                    'height': height,
                    'hash': hash,
                    'Size': Size,
                    'seed': seed,
                    'Model': Model,
                    'steps': steps,
                    'prompt': prompt,
                    'sampler': sampler,
                    'cfgScale': cfgScale,
                    'resources': resources,
                    'Clip skip': Clipskip,
                    'Hires upscale': Hiresupscale,
                    'Hires upscaler': Hiresupscaler,
                    'negativePrompt': negativePrompt,
                    'Denoising strength': Denoisingstrength
                }

                # 将当前图片信息添加到列表
                all_images_info.append(image_info)
            downloadUrl = modelVersions.get('downloadUrl')
            modelVersiones_info = {
                'id': modelVersions_id,
                'modelId': modelVersions_modelId,
                'name': modelVersions_name,
                'createdAt': modelVersions_createdAt,
                'updatedAt': modelVersions_updatedAt,
                'trainedWords': modelVersions_trainedWords,
                'baseModel': modelVersions_baseModel,
                'earlyAccessTimeFrame': modelVersions_earlyAccessTimeFrame,
                'description': modelVersions_description,
                'stats': {
                    'downloadCount': stats_downloadCount,
                    'ratingCount': stats_ratingCount,
                    'rating': stats_rating
                },
                'files': [
                    {
                        'name': files_name,
                        'id': files_id,
                        'sizeKB': files_sizeKB,
                        'type': files_type,
                        'metadata': {
                            'fp': metadata_fp,
                            'size': metadata_size,
                            'format': metadata_format
                        },
                        'pickleScanResult': files_pickleScanResult,
                        'pickleScanMessage': files_pickleScanMessage,
                        'virusScanResult': files_virusScanResult,
                        'scannedAt': files_scannedAt,
                        'hashes': {
                            'AutoV2': hashes_AutoV2,
                            'SHA256': hashes_SHA256,
                            'CRC32': hashes_CRC32,
                            'BLAKE3': hashes_BLAKE3
                        },
                        'downloadUrl': files_downloadUrl,
                        'primary': files_primary
                    }
                ],
                'images': all_images_info,
                'downloadUrl':downloadUrl
            }
            all_modelVersiones_info.append(modelVersiones_info)

        folder_name = 'models'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        model_id = model.get('id')

        # 创建以model_id命名的文件
        file_path = os.path.join(folder_name, f'{model_id}.txt')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("Model ID: " + str(model_id) + "\n")
            file.write("Model Name: " + str(model_name) + "\n")
            file.write("Model Description: " + str(model_description) + "\n")
            file.write("Model Type: " + str(model_type) + "\n")
            file.write("NSFW: " + str(nsfw) + "\n")
            file.write("Allow No Credit: " + str(allow_no_credit) + "\n")
            file.write("Allow Commercial Use: " + str(allow_commercial_use) + "\n")
            file.write("Allow Derivatives: " + str(allow_derivatives) + "\n")
            file.write("Creator Username: " + str(creator_username) + "\n")
            file.write("Download Count: " + str(download_count) + "\n")
            file.write("Favorite Count: " + str(favorite_count) + "\n")
            file.write("Comment Count: " + str(comment_count) + "\n")
            file.write("Rating Count: " + str(rating_count) + "\n")
            file.write("Rating: " + str(rating) + "\n")
            file.write("Tags: " + str(tags) + "\n")

            for model_version_info in all_modelVersiones_info:
                file.write("Model Version Data:\n")
                for key, value in model_version_info.items():
                    if key == 'images':
                        file.write(f"{key}:\n")
                        for image_info in value:
                            for k, v in image_info.items():
                                file.write(f"\t{k}: {v}\n")
                    elif key == 'stats':
                        file.write(f"{key}:\n")
                        for stat_key, stat_value in value.items():
                            file.write(f"\t{stat_key}: {stat_value}\n")
                    elif key == 'files':
                        file.write(f"{key}:\n")
                        for file_info in value:
                            for file_key, file_value in file_info.items():
                                if file_key == 'metadata':
                                    file.write("\tMetadata:\n")
                                    for meta_key, meta_value in file_value.items():
                                        file.write(f"\t\t{meta_key}: {meta_value}\n")
                                elif file_key == 'hashes':
                                    file.write("\tHashes:\n")
                                    for hash_key, hash_value in file_value.items():
                                        file.write(f"\t\t{hash_key}: {hash_value}\n")
                                else:
                                    file.write(f"\t{file_key}: {file_value}\n")
                    else:
                        file.write(f"{key}: {value}\n")
            time.sleep(2)  # 休息2秒

def worker():
    while True:
        with lock:
            current_page = page_queue.get()
        if current_page is None:
            break
        fetch_data(current_page)
        page_queue.task_done()

# 创建队列以在多个线程间分发工作
page_queue = queue.Queue()

# 将页面编号添加到队列中
for page in range(1, total_pages + 1):
    page_queue.put(page)

# 创建并启动多个线程
num_threads = 10  # 线程数量
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

# 等待所有页面请求处理完成
page_queue.join()

# 通知线程退出
for _ in range(num_threads):
    page_queue.put(None)

# 等待所有线程完成
for thread in threads:
    thread.join()
