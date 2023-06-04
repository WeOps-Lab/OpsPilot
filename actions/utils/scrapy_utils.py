import scrapy
from scrapy.crawler import CrawlerProcess


class WebSiteSpider(scrapy.Spider):
    name = "website"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        titles = response.xpath(self.title_path).extract()
        for title in titles:
            entity = {'title': title}
            self.data.append(entity)
        return titles


def fetch_website(url, title_path):
    data = []
    crawler = CrawlerProcess()
    crawler.crawl(WebSiteSpider, url=url, title_path=title_path, data=data)
    crawler.start()
    crawler.join()
    return data
