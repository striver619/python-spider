import scrapy
from scrapy.http import Request
from urllib import parse
from youyd_spider.items.FangTianXiaSpiderItem import FangTianXiaItemLoader, FangTianXiaSpiderItem
import time

"""
爬虫
"""


class zhipin(scrapy.Spider):
    name = "zhipin"
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101050100/?query=python']

    def parse(self, response):
        details = response.css('.job-list > ul > li')
        for detail in details:
            image_url = "xxxx"
            post_url = detail.css("div.nlc_details > div.house_value > div.nlcd_name > a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front_image_url": image_url},
                          callback=self.parse_detail)

    def parse_detail(self, response):
        """
        解析页面详情页，使用 item_loader 参考：https://www.cnblogs.com/qingyunzong/p/9945174.html
        :param response: 下载完的页面回调
        :return: item
        """
        item = FangTianXiaSpiderItem()
        item['pid'] = response.css(
            'div.info-primary>h3>a::attr(data-jid)').extract_first().strip()
        item['positionName'] = response.css(
            'div.response-title::text').extract_first().strip()
        item['salary'] = response.css(
            'div.info-primary>h3>a> span::text').extract_first().strip()

        info_primary = response.css('div.info-primary>p::text').extract()
        item['city'] = info_primary[0].strip()
        item['workYear'] = info_primary[1].strip()
        item['education'] = info_primary[2].strip()

        item['companyShortName'] = response.css(
            'div.company-text>h3>a::text').extract_first().strip()
        company_info = response.css('div.company-text>p::text').extract()
        if len(company_info) == 3:
            item['industryField'] = company_info[0].strip()
            item['financeStage'] = company_info[1].strip()
            item['companySize'] = company_info[2].strip()

        item['time'] = response.css(
            'div.info-publis>p::text').extract_first().strip()
        interviewer_info = response.css('div.info-publis>h3::text').extract()
        item['interviewer'] = interviewer_info[1]

        item['updated_at'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        yield item
