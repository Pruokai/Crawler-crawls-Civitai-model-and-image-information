# 爬虫爬取[Civitai](https://civitai.com/)中的模型或者图片信息
## 技术文档指导:[https://github.com/civitai/civitai/wiki/REST-API-Reference#get-apiv1modelsmodelid](https://github.com/civitai/civitai/wiki/REST-API-Reference#get-apiv1modelsmodelid)
## 图片信息爬取，运行civitai_images.py，会把爬取的每一张图片信息都以image_id.txt的形式存储在images文件夹下，方便进行查重，如果想要根据自己的需求修改爬取的内容，可以参考技术文档指导自行修改。
## 模型信息爬取，运行civitai_models.py，会把爬取的每一个模型信息都以model——name.txt的形式存储在models文件夹下，方便进行查重，如需修改内容，同上。
