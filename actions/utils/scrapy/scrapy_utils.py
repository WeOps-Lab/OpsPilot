from scrapy.crawler import CrawlerProcess

from actions.utils.scrapy.spiders.OSChinaNewsSpider import OSChinaNewsSpider


def call_oschina_news_spider():
    data = []
    crawler = CrawlerProcess()
    crawler.crawl(OSChinaNewsSpider, data=data)
    crawler.start()
    crawler.join()
    return data
