import logging
import random

logger = logging.getLogger(__name__)

'''
ip代理
'''


class RandomProxyIpMiddleware(object):

    PROXIES = [
        "http://47.105.149.144:3128"
    ]

    """
    动态设置代理服务器的IP 地址
    """

    def process_request(self, request, spider):
        ip = random.choice(self.PROXIES)
        request.meta["proxy"] = ip
