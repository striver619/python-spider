# -*- coding: utf-8 -*-

import datetime
import re
from scrapy.loader import ItemLoader

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def add_jobbole(value):
    return value + "-GuoGuang"


def date_convert(value):
    """
    string转化成date
    :param value:
    :return:
    """
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def get_nums(value):
    """
    正则提取value中的数字
    :param value:
    :return:
    """
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def return_value(value):
    return value


def remove_comment_tags(value):
    """
    去掉tag中提取的评论
    :param value:
    :return:
    """
    if "评论" in value:
        return ""
    else:
        return value


class FangTianXiaItemLoader(ItemLoader):
    """
    继承ItemLoader，指定所有字段的默认输出使用TakeFirst函数
    TakeFirst获取list中的第一个值
    """
    default_output_processor = TakeFirst()


class FangTianXiaSpiderItem(scrapy.Item):
    """
    封装字段，类似Java实体类
    """
    name = scrapy.Field()
    # String拼接
    # demo = scrapy.Field(lambda x:x+"-jobble", add_jobbole)
    price = scrapy.Field(input_processor=MapCompose(get_nums))
    front_image_url = scrapy.Field(output_processor=MapCompose(return_value))

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO house(name,price) VALUES(%s,%s)
                    """

        fron_image_url = ""
        # content = remove_tags(self["content"])

        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["name"], self["price"])
        return insert_sql, params
