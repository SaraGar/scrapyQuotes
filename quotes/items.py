import scrapy


class QuotesItem(scrapy.Item):   
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    
