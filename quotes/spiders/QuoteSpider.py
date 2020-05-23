# -*- coding: utf-8 -*-
import scrapy


class QuotespiderSpider(scrapy.Spider):
    name = 'QuoteSpider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
