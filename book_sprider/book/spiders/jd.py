# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 大分类列表
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item['b_cate'] = dt.xpath("./a/text()").extract_first()
            # //a[@id='3']/following-sibling::a[1]
            # 小分类列表
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            for em in em_list:
                item['s_cate'] = em.xpath("./a/text()").extract_first()
                item['s_href'] = em.xpath("./a/@href").extract_first()
                # https://list.jd.com/list.html?cat=1713,11745,11751&tid=11751
                if item['s_href'] is not None:
                    item['s_href'] = "https:" + item['s_href']
                    yield scrapy.Request(
                        url=item['s_href'],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta.get('item')
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item['book_img'] = li.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            if item['book_img'] is None:
                item['book_img'] = li.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            # http://img11.360buyimg.com/n7/jfs/t1/99898
            item['book_img'] = "http:" + item['book_img']

            item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first()
            item["book_author"] = li.xpath(".//span[@class='author_type_1']/a/text()").extract_first()
            item["book_store"] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            # 价格ID
            item['data-sku'] = li.xpath("./div/@data-sku").extract_first()

            yield scrapy.Request(
                url="https://p.3.cn/prices/mgets?skuIds=J_{}".format(item['data-sku']),
                callback=self.parse_book_price,
                meta={"item": deepcopy(item)}
            )


        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = "http://list.jd.com" + next_url
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_book_list,
                meta={"item": deepcopy(item)}
            )

    def parse_book_price(self, response):
        item = response.meta.get('item')
        item['book_price'] = json.loads(response.text)[0]['op']
        # book_price = json.loads(response.text)[0]['m']
        # print(type(item['book_price']))
        # print(book_price)
        # print(item)
        yield item











