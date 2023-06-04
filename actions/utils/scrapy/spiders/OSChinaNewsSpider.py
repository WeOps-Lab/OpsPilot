import scrapy
from scrapy import Item, Field


class OSChinaNewsInfo(Item):
    title = Field()


class OSChinaNewsSpider(scrapy.Spider):
    name = "oschina_news"
    start_urls = ['https://www.oschina.net/news/widgets/_news_index_generic_list_new?p=1&type=ajax']

    def parse(self, response):
        titles = response.xpath('/html/body/div[1]/div/div/h3/div/text()').extract()
        for title in titles:
            item = OSChinaNewsInfo()
            item['title'] = title
            self.data.append(item)
            yield item
