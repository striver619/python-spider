# -*- coding: utf-8 -*-

import os

BOT_NAME = 'youyd_spider'

SPIDER_MODULES = ['youyd_spider.spiders']
NEWSPIDER_MODULE = 'youyd_spider.spiders'

# 通过在用户代理上标识自己（和您的网站）来负责任地进行爬网
# USER_AGENT = 'youyd_spider (+http://www.yourdomain.com)'

# 遵守robots.txt规则
ROBOTSTXT_OBEY = False

# 配置Scrapy执行的最大并发请求数（默认值：16）
# CONCURRENT_REQUESTS = 32

# 配置同一网站的请求延迟（默认值：0）
# DOWNLOAD_DELAY = 3
# 下载延迟设置将仅接受以下一项
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# 禁用cookie（默认情况下启用）
COOKIES_ENABLED = False

# 禁用Telnet控制台（默认情况下启用）
# TELNETCONSOLE_ENABLED = False

# 覆盖默认的请求头：
DEFAULT_REQUEST_HEADERS = {
    ":authority": "www.zhipin.com",
    ":method": "GET",
    ":path": "/c101050100/?query=python",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "cookie": "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1602346079; lastCity=100010000; __g=-; __c=1602346081; __l=l=%2Fwww.zhipin.com%2Fc101050100%2F%3Fquery%3Dpython&r=&g=&friend_source=0&friend_source=0; __a=34277735.1602346081..1602346081.3.1.3.3; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1602346108; __zp_stoken__=d494bPAMEGWd8Xm98eTtNCVg%2BXDEZamIgUCckNxpJeRAvJDFNDGdoIhxgIG9mEDxNFyA2UWEuckpXVUoXezY5Z3wGEzxQAid2OVNwcDVAARZlDwwcKlpTQz9MFUtBMkBxEXE8QlwGfUN8XHV0dA%3D%3D",
    "pragma": "no-cache",
    "referer": "https://www.zhipin.com/web/common/security-check.html?seed=R3kZvruq209Z7QJ8BL6Ad%2BMEeA8ENi%2BTEBz8H1AMA9M%3D&name=35077fad&ts=1602346078211&callbackUrl=%2Fc101050100%2F%3Fquery%3Dpython&srcReferer=",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}
# 启用或禁用蜘蛛中间件
# SPIDER_MIDDLEWARES = {
#    'youyd_spider.middlewares.ArticlespiderSpiderMiddleware': 543,
# }

# 启用或禁用下载器中间件
DOWNLOADER_MIDDLEWARES = {
    # 'youyd_spider.middlewares.MyCustomDownloaderMiddleware': 543,
    'youyd_spider.middlewares.rotate_user_agent.RandomUserAgentMiddleware': 400,
}
JSONRPC_ENABLED = True

# 启用或禁用扩展
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }


# 配置项目管道 item pipelines
# 指定spider运行流程 执行哪些pipeline
ITEM_PIPELINES = {
    'youyd_spider.pipelines.JsonExporterPipeLine': 1,
    # 'youyd_spider.pipelines.ExcelPipeline': 2,
    #  'scrapy.pipelines.images.ImagesPipeline': 1,
    #  'youyd_spider.pipelines.ArticleImagePipeline': 2,
    # 'youyd_spider.pipelines.MysqlPipeLine': 2,
    #  'youyd_spider.pipelines.ElasticSearchPipeline': 5

}
IMAGES_URLS_FIELD = "front_image_url"
project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir, 'images')

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.join(BASE_DIR, 'AritcleSpider'))

#
# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100

# 启用和配置AutoThrottle扩展（默认情况下禁用）
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# 初始下载延迟
AUTOTHROTTLE_START_DELAY = 5
# 高延迟时要设置的最大下载延迟
AUTOTHROTTLE_MAX_DELAY = 60
# Scrapy应该并行发送的平均请求数
# 每个远程服务器
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 启用显示收到的每个响应的节流统计信息：
AUTOTHROTTLE_DEBUG = False
DOWNLOAD_DELAY = 3

# 启用和配置HTTP缓存（默认情况下禁用）
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 配置数据库连接
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

ES_HOST = "39.108.191.56"
