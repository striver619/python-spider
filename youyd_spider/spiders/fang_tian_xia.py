import re
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
import time
from youyd_spider.items import FangTianXiaSpiderItem, ArticleItemLoader
from youyd_spider.utils.common import get_md5

"""
房天下爬虫
REF：https://zhuanlan.zhihu.com/p/48047813
    https://ovwane.icu/2017/05/01/Python%E5%88%86%E5%B8%83%E5%BC%8F%E7%88%AC%E8%99%AB%E6%89%93%E9%80%A0%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E-%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/#
    https://blog.csdn.net/qq_35394891/article/details/82952774
    
NOTE：由于房天下 "下一页" 逻辑是到最后五页隐藏下一页摁钮 所以我这里省略掉，需要的同学可以自行处理此逻辑

Scrapy 爬虫运作流程
1 引擎：Hi！Spider, 你要处理哪一个网站？
2 Spider：老大要我处理xxxx.com。
3 引擎：你把第一个需要处理的URL给我吧。
4 Spider：给你，第一个URL是xxxxxxx.com。
5 引擎：Hi！调度器，我这有request请求你帮我排序入队一下。
6 调度器：好的，正在处理你等一下。
7 引擎：Hi！调度器，把你处理好的request请求给我。
8 调度器：给你，这是我处理好的request
9 引擎：Hi！下载器，你按照老大的下载中间件的设置帮我下载一下这个request请求
10 下载器：好的！给你，这是下载好的东西。（如果失败：sorry，这个request下载失败了。然后引擎告诉调度器，这个request下载失败了，你记录一下，我们待会儿再下载）
11 引擎：Hi！Spider，这是下载好的东西，并且已经按照老大的下载中间件处理过了，你自己处理一下（注意！这儿responses默认是交给def parse()这个函数处理的）
12 Spider：（处理完毕数据之后对于需要跟进的URL），Hi！引擎，我这里有两个结果，这个是我需要跟进的URL，还有这个是我获取到的Item数据。
13 引擎：Hi ！管道 我这儿有个item你帮我处理一下！调度器！这是需要跟进URL你帮我处理下。然后从第四步开始循环，直到获取完老大需要全部信息。
14 管道``调度器：好的，现在就做！
"""
class FangtianxiaSpider(scrapy.Spider):
    name = "FangTianXia"
    allowed_domains = ['fang.com']
    start_urls = ['https://wf.newhouse.fang.com/house/s/']

    def parse(self, response):
        """
        1. 获取数据列表页中的url列表并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        """

        #解析列表页中的所有url并交给scrapy下载后并进行解析
        post_nodes = response.css("#newhouse_loupai_list > ul li")
        for post_node in post_nodes:
            image_url = "xxxx"
            post_url = post_node.css("div.nlc_details > div.house_value > div.nlcd_name > a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url = response.xpath("//div[@class='page']//a[@class='next'][last()]/@href").get()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        """
        解析页面详情页，使用 item_loader 参考：https://www.cnblogs.com/qingyunzong/p/9945174.html
        :param response: 下载完的页面回调
        :return: item
        """
        item = FangTianXiaSpiderItem()
        front_image_url = response.meta.get("front_image_url", "")  # 封面图
        item_loader = ArticleItemLoader(item=FangTianXiaSpiderItem(), response=response)
        item_loader.add_xpath("name", "//div[@class='tit']//h1//strong/text()")
        item_loader.add_xpath("price", "//div[contains(@class,'inf_left fl')]//span[@class='prib cn_ff']/text()")
        item_loader.add_value("front_image_url", front_image_url)
        item = item_loader.load_item()
        yield item
