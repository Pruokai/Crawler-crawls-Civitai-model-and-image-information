# 爬虫爬取[Civitai](https://civitai.com/)中的模型或者图片信息
## [技术文档指导](https://github.com/civitai/civitai/wiki/REST-API-Reference#get-apiv1modelsmodelid):[https://github.com/civitai/civitai/wiki/REST-API-Reference#get-apiv1modelsmodelid](https://github.com/civitai/civitai/wiki/REST-API-Reference#get-apiv1modelsmodelid)
## 图片信息爬取，运行civitai_images.py，会把爬取的每一张图片信息都以image_id.txt的形式存储在images文件夹下，方便进行查重，如果想要根据自己的需求修改爬取的内容，可以参考[技术文档指导](https://github.com/civitai/civitai/wiki/REST-API-Reference#get-apiv1modelsmodelid)自行修改。
## 模型信息爬取，运行civitai_models.py，会把爬取的每一个模型信息都以model_id.txt的形式存储在models文件夹下，方便进行查重，如需修改内容，同上。

## 11.6更新：
### 爬取模型和图片速度较慢，修改为多线程爬取，可以根据需求修改num_threads = 10，max_workers=10线程数量，但也别太大。

## 11.9更新：
### 1.增添获取所有模型与图片大小功能：models_size.py和images_size.py；
### 2.增添下载模型与图片功能：models_download.py和images_download.py；
### 3.增添建表功能：一级类目表primary_category.py包含模型基本信息，二级类目表secondary_category.py包含模型各个版本的信息，三级类目表tertiary_category.py包含每个版本的多张例图的信息，其中一级类目表和二级类目表的连接桥梁为Model ID，二级类目表和三级类目表的连接桥梁为name，
### 注意：因为我是全量爬取，所以三级类目表图片信息过多容易内存爆炸或者超出xlsx表格上限，所以我通过file_segmentation.py将models文件夹分为多个个文件夹，每个文件夹有10000个txt文件，再运行tertiary_category.py，tertiary_category.py中我对多个文件夹使用了循环，如果你不需要可以自行修改。
