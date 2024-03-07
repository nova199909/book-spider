# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider


class YgSpider(RedisCrawlSpider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    # start_urls = ['http://sun0769.com/']
    redis_key = 'yg'


    rules = (
        # follow all links
        # 列表页面
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='title-state-ul']/li"), callback='parse_page'),
        # 列表页面翻页
        Rule(LinkExtractor(restrict_xpaths="//a[@class='arrow-page prov_rota']"), follow=True),
    )

    def parse_page(self, response):
        item = {}
        item['content'] = response.xpath("//div[@class='details-box']/pre/text()").extract()
        print(item)
