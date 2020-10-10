import scrapy
from scrapy.http import Request
from urllib import parse
from youyd_spider.items.FangTianXiaSpiderItem import FangTianXiaItemLoader,FangTianXiaSpiderItem

"""
房天下爬虫
REF：https://zhuanlan.zhihu.com/p/48047813
    https://ovwane.icu/2017/05/01/Python%E5%88%86%E5%B8%83%E5%BC%8F%E7%88%AC%E8%99%AB%E6%89%93%E9%80%A0%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E-%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/#
    https://blog.csdn.net/qq_35394891/article/details/82952774
NOTE：由于房天下 "下一页" 逻辑是到最后五页隐藏下一页摁钮 所以我这里省略掉，需要的同学可以自行处理此逻辑
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
        details = response.css("#newhouse_loupai_list > ul li")
        for detail in details:
            image_url = "xxxx"
            post_url = detail.css("div.nlc_details > div.house_value > div.nlcd_name > a::attr(href)").extract_first("")
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
        item_loader = FangTianXiaItemLoader(item=FangTianXiaSpiderItem(), response=response)
        item_loader.add_xpath("name", "//div[@class='tit']//h1//strong/text()")
        item_loader.add_xpath("price", "//div[contains(@class,'inf_left fl')]//span[@class='prib cn_ff']/text()")
        item_loader.add_value("front_image_url", front_image_url)
        item = item_loader.load_item()
        yield item
