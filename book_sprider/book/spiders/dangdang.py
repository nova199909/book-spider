# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from copy import deepcopy


class DangdangSpider(RedisCrawlSpider):
    name = 'dangdang'
    # name = 'mycrawler_redis'
    # redis_key = 'mycrawler:start_urls'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://dangdang.com/']
    redis_key = "dangdang"

    def parse(self, response):
        div_list = response.xpath("//div[@class='con flq_body']/div")
        for div in div_list:
            item = {}
            item['b_cate'] = div.xpath("./dl/dt//text()").extract()
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip()) > 0]
            dl_list = div.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:
                item['m_cate'] = dl.xpath("./dt//text()").extract()
                item['m_cate'] = [i.strip() for i in item['m_cate'] if len(i.strip()) > 0]

                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    item['s_href'] = a.xpath("./@href").extract_first()
                    item['s_cate'] = a.xpath("./@title").extract_first()

                    yield scrapy.Request(
                        url=item['s_href'],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        pass




