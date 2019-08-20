# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Response


class ScepticalscienceSpider(scrapy.Spider):
    name = 'scepticalscience'
    allowed_domains = ['skepticalscience.com', 'sks.to']
    start_urls = ['https://skepticalscience.com/shorturls.php']

    def parse(self, response : Response):
        pages = response.css('td::text').re(r'.*sks\.to.*')

        for p in pages:
            yield scrapy.Request(p, callback=self.parse_page)

    def parse_page(self, response : Response):
        x = response.css('div#mainbody > p').getall()

        from bs4 import BeautifulSoup

        l = []


        for q in x:
            bs = BeautifulSoup(q)

            bs = re.sub('\s\s+', ' ', bs.text)
            l.append(bs)

        yield {
            'url': response.url,
            'text': ' '.join(l)
        }
