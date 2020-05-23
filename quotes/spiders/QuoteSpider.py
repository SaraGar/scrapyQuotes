import os
import re
import codecs
import scrapy

from quotes.items import QuotesItem
class QuotespiderSpider(scrapy.Spider):
    ext = '.txt' #results file extension
    wholeSite = True #scan the whole site or not
    fn = 'quotes.toscrape' #results file name, same that url
    dn = fn + '.com' #domain name
    firstPage = ['http://'+dn] #first page to scan
    scope = [
        'http://' + dn + '/page/1',
        'http://' + dn + '/page/2',
        'http://' + dn + '/page/3',
        'http://' + dn + '/page/4',
    ] #pages to scan is wholeSite is set to False

    name = 'QuoteSpider'
    allowed_domains = [dn]
    start_urls = [dn]

    """ 
        Delete results file if exists, so it can be refreshed each time 
    """
    def delFile(self):
        if os.path.exists(self.fn + self.ext):
            os.remove(self.fn + self.ext)

    """
        Call delFile and make the requests
    """
    def  start_requests(self):
        self.delFile()
        pages = self.firstPage if self.wholeSite else self.scope

        for page in pages:
            yield scrapy.Request(page, self.parse)
   
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

    def parse(self, response):
        self.extractData(response)

        #We need to get the 'next page' link, only in case wholeSite = true
        if self.wholeSite:
            next = response.css('li.next > a::attr(href)').extract_first()
            if next is not None:
                yield scrapy.Request(response.urljoin(next))
    """
        Writes the text in a file, with proper format
    """
    def writeTxt(self, q):
        with codecs.open(self.fn + self.ext, 'a+', 'utf-8') as f:
            f.write(q["quote"]+ '\r\n')
            f.write(q["author"]+ '\r\n')
            f.write(q["tags"]+ '\r\n\n')