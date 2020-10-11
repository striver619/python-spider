# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

import scrapy


class ZhiPinItemLoader(ItemLoader):
    """
    继承ItemLoader，指定所有字段的默认输出使用TakeFirst函数
    TakeFirst获取list中的第一个值
    """
    default_output_processor = TakeFirst()


class ZhiPinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 职位id
    pid = scrapy.Field()
    # 职业名称
    positionName = scrapy.Field()
    # 求职发布者
    interviewer = scrapy.Field()
    # 工作年限
    workYear = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 文凭要求
    education = scrapy.Field()
    # 公司名称
    companyShortName = scrapy.Field()
    # 工作领域
    industryField = scrapy.Field()
    # 上市情况
    financeStage = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 更新时间
    updated_at = scrapy.Field()
    # 职位详情
    detail = scrapy.Field()
    # 工作地点
    location = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO zhipin(pid,positionName,interviewer,workYear,salary,
                        city,education,companyShortName,industryField,financeStage,
                        companySize,time,updated_at,detail,location) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        params = (self["pid"], self["positionName"],
                  self["interviewer"], self["workYear"],
                  self["salary"], self["city"],
                  self["education"], self["companyShortName"],
                  self["industryField"], self["financeStage"],
                  self["companySize"], self["time"],
                  self["updated_at"], self["detail"],
                  self["location"]
                  )
        return insert_sql, params
