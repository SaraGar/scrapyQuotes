import os
import re
import codecs
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from quotes.items import QuotesItem

class QuotecrawlerSpider(CrawlSpider):

    ext = '.txt' #results file extension
    fn = 'quotes.toscrape' #results file name, same that url
    dn = fn + '.com' #domain name
   
    name = 'QuoteCrawler'
    allowed_domains = [dn]
    start_urls = ['http://' +dn]

    rules = (
        Rule(LinkExtractor(restrict_css='li.next'), callback='parse_page', follow=True),
       #Rule(LinkExtractor(allow=r'tag/'), callback='parse_page', follow=True),
    )

    """
        Writes the text in a file, with proper format
    """
    def writeTxt(self, q):
        with codecs.open(self.fn + self.ext, 'a+', 'utf-8') as f:
            f.write(q["quote"]+ '\r\n')
            f.write(q["author"]+ '\r\n')
            f.write(q["tags"]+ '\r\n\n')

    """
        Get the specific data from the response, and call writeText
    """
    def extractData(self, response):
        q = QuotesItem()

        for quote in response.css('div.quote'):
            q['quote'] = '"'+ re.sub(r'[^\x00-\x7f]', r'', quote.css('span.text::text').extract_first()) +'"'
            q['author'] = quote.css('small.author::text').extract_first()
            q['tags'] = ' '.join(str(s) for s in quote.css('div.tags > a.tag::text').extract())

            self.writeTxt(q)

    def parse_page(self, response):
       self.extractData(response)
