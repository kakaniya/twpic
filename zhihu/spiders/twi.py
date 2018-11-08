# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pyquery import PyQuery as pq
import json
import re
import requests

class TwiSpider(scrapy.Spider):
    name = 'twi'
    allowed_domains = ['twitter.com']
    start_urls = ['https://twitter.com/']

    url = 'https://twitter.com/granbluefantasy'
    get_url = 'https://twitter.com/i/profiles/show/granbluefantasy/timeline/tweets?include_available_features=1&include_entities=1&max_position={max_position}&reset_error_state=false'
    max_position = 'xxxxxxxxxxxx'
    filename = 0

    def start_requests(self):
        yield Request(self.url,callback=self.parse_pageone)
        yield Request(self.get_url.format(max_position=self.max_position),callback=self.parse_getposition)

    def parse_pageone(self, response):
        html = pq(response.text)
        imgs = html('.AdaptiveMedia-photoContainer img')
        for img in imgs.items():
            pic_source = requests.get(img.attr('src'))
            with open('路径' + str(self.filename) + 'f.jpg', 'wb') as f:
                f.write(pic_source.content)
                f.close()
            self.filename += 1

    def parse_getposition(self, response):
        results = json.loads(response.text)
        image_find = re.compile('data-image-url="(.*?)"')
        for result in image_find.findall(results.get('items_html')):
#            print(result)
            pic_source = requests.get(result)
            with open('路径'+str(self.filename)+'.jpg','wb') as f:
                f.write(pic_source.content)
                f.close()
            self.filename += 1

        min_position = results.get('min_position')
        yield Request(self.get_url.format(max_position=min_position),callback=self.parse_getposition)
