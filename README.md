<h1 align="center">Welcome to python_spider 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-Python 3.7-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/scrapy/scrapy">
    <img alt="scrapy" src="https://img.shields.io/badge/scrapy-success.svg" target="_blank" />
  </a>
  <a href="https://github.com/GuoGuang0536/python_spider/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/GuoGuang">
    <img alt="Twitter: GuoGuang0536" src="https://img.shields.io/twitter/follow/GuoGuang.svg?style=social" target="_blank" />
  </a>
</p>

> Scrapy Spider

### 🏠 YOUYD_SPIDER

爬虫项目逐渐增加中...
- 房天下
- Boss直聘
...



## Prerequisites

- python3
- scrapy
    [Scrapy 框架入门简介](https://segmentfault.com/a/1190000013178839/)
    
    ![image](https://image-static.segmentfault.com/8c/59/8c591d54457bb033812a2b0364011e9c_articlex)

### Scrapy 爬虫运作流程
1. 引擎：Hi！Spider, 你要处理哪一个网站？
2. Spider：老大要我处理xxxx.com。
3. 引擎：你把第一个需要处理的URL给我吧。
4. Spider：给你，第一个URL是xxxxxxx.com。
5. 引擎：Hi！调度器，我这有request请求你帮我排序入队一下。
6. 调度器：好的，正在处理你等一下。
7. 引擎：Hi！调度器，把你处理好的request请求给我。
8. 调度器：给你，这是我处理好的request
9. 引擎：Hi！下载器，你按照老大的下载中间件的设置帮我下载一下这个request请求
10. 下载器：好的！给你，这是下载好的东西。（如果失败：sorry，这个request下载失败了。然后引擎告诉调度器，这个request下载失败了，你记录一下，我们待会儿再下载）
11. 引擎：Hi！Spider，这是下载好的东西，并且已经按照老大的下载中间件处理过了，你自己处理一下（注意！这儿responses默认是交给def parse()这个函数处理的）
12. Spider：（处理完毕数据之后对于需要跟进的URL），Hi！引擎，我这里有两个结果，这个是我需要跟进的URL，还有这个是我获取到的Item数据。
13. 引擎：Hi ！管道 我这儿有个item你帮我处理一下！调度器！这是需要跟进URL你帮我处理下。然后从第四步开始循环，直到获取完老大需要全部信息。
14. 管道``调度器：好的，现在就做！


## Install

```sh
git clone https://github.com/GuoGuang/python_spider.git
```

## Usage

```bash

scrapy crawl {project/spiders/className}

# demo
scrapy crawl FangTianXia
```

如果需要执行爬虫数据存储方式请修改 settings.py-->ITEM_PIPELINES配置，默认以JSON格式保存在当前路径下且保存到数据库

## Author

👤 **GuoGuang**

* Twitter: [@GuoGuang](https://twitter.com/GuoGuang)
* Github: [@GuoGuang](https://github.com/GuoGuang)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/GuoGuang/python_spider/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [GuoGuang](https://github.com/GuoGuang).<br />
This project is [GuoGuang](mit) licensed.