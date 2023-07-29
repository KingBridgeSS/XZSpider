# XZSpider
[先知社区](https://xz.aliyun.com/)爬虫，支持异步下载，更新文章URL，并把文章以离线markdown格式保存到本地。

# Usage

1. 更新 URLs

`python3 update_list.py`

运行后程序会把上次爬取的URL保存到previous_list.json，本次爬取的所有文章URL保存在list.json，并求差集保存到diff_list.json以供下载。

2. 下载

```
Usage: python3 download.py -d <save_path>
Options:
-d <save_path>  Specify the save path for downloaded files (if not specified, download to ./downloads)
-h              Show this help message
```

# TODOs

- [x] 提供进度条
- [x] 异步下载（线程池）
- [ ] 异步更新URL