# -*- coding: utf-8 -*-
import codecs
import json

import MySQLdb
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import pymysql
from w3lib.html import remove_tags
import logging
from openpyxl import Workbook

from youyd_spider.models.models import Article

"""
项目管道文件，如：一般结构化的数据持久化
"""


logger = logging.getLogger(__name__)

class YouydSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipeLine(object):
    """
    调用scrapy提供的json export导出json文件
    """
    def __init__(self):

        logger.info("JsonExporterPipeLine：自定义json导出__init__")
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        logger.info("spider_closed：关闭爬虫")
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        logger.info("process_item：执行写入操作")
        return item


class ExcelPipeline(object):
    """
        导出数据到Excel
    """
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws_clean_data = self.wb.create_sheet("清洗数据")
        self.ws_clean_data.append(['姓名', '年龄', '性别', '身份证'])

    def process_item(self, item, spider):
        line = [item['name'], item['price']]
        self.ws_clean_data.append(line)
        self.wb.save('./test.xlsx')
        return item


class MysqlPipeLine(object):
    """
    写入到mysql中。
    在 settings.py 中指定该功能是否启用
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            # auth_plugin='mysql_native_password',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        print (insert_sql, params)
        cursor.execute(insert_sql, params)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item


class ElasticSearchPipeline(object):
    """
    写入数据到es中
    """
    def analyze_tokens(self, text):
        from models.models import connections
        es = connections.get_connection(Article._doc_type.using)
        index = Article._doc_type.index

        if not text:
            return []
        global used_words
        result = es.indices.analyze(index=index, analyzer='ik_max_word',
                                    params={'filter': ['lowercase']}, body=text)

        words = set([r['token'] for r in result['tokens'] if len(r['token']) > 1])

        new_words = words.difference(used_words)
        used_words.update(words)
        return new_words

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def gen_suggests(self, title, tags):
        global used_words
        used_words = set()
        suggests = []

        for item, weight in ((title, 10), (tags, 3)):
            item = self.analyze_tokens(item)
            if item:
                suggests.append({'input': list(item), 'weight': weight})
        return suggests

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings
        Article.init()
        return ext


    def process_item(self, item, spider):
        article = Article()
        article.title = item["title"]
        article.create_date = item["create_date"]
        article.content = remove_tags(item["content"]).strip().replace("\r\n","").replace("\t","")
        article.front_image_url = item["front_image_url"]
        # article.front_image_path = item["front_image_path"]
        article.praise_nums = item["praise_nums"]
        article.comment_nums = item["comment_nums"]
        article.fav_nums = item["fav_nums"]
        article.url = item["url"]
        article.tags = item["tags"]
        article.id = item["url_object_id"]

        title_suggest = self.gen_suggests(article.title, article.tags)
        article.title_suggest = title_suggest

        article.save()

        return item