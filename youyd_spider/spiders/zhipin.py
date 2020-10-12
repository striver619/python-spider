import scrapy
from scrapy.http import Request
from urllib import parse
from youyd_spider.items.ZhipinItem import ZhiPinItemLoader, ZhiPinItem
import time

"""
爬虫  
"""


class zhipin(scrapy.Spider):
    name = "zhipin"
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101050100/?query=python']

    def parse(self, response):
        print("proxy-->", response.meta['proxy'])
        print("User-Agent-->", response.request.headers['User-Agent'])
        details = response.xpath("//div[@class='job-list']/ul//li")
        for detail in details:
            image_url = "xxxx"
            detail_url = detail.xpath("//*[@id='main']/div/div[2]/ul/li[1]/div/div[1]/div[1]/div/@href").get()
            yield Request(url=parse.urljoin(response.url, detail_url),
                          meta={"front_image_url": image_url},
                          callback=self.parse_detail)

    def parse_detail(self, response):

        item_loader = ZhiPinItemLoader(item=ZhiPinItem(), response=response)
        item_loader.add_xpath("pid", "//*[@id='main']/div[3]/div/div[1]/div[2]/div/a[2]/@href")

        item = item_loader.load_item()
        yield item
